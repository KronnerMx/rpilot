#!/usr/bin/env python
from cereal import car, log
from common.realtime import sec_since_boot
from selfdrive.config import Conversions as CV
from selfdrive.controls.lib.drive_helpers import create_event, EventTypes as ET
from selfdrive.controls.lib.vehicle_model import VehicleModel
from selfdrive.car.vw.values import DBC, CAR
from selfdrive.car.vw.carstate import CarState, get_gateway_can_parser, get_extended_can_parser
from common.params import Params

try:
  from selfdrive.car.vw.carcontroller import CarController
except ImportError:
  CarController = None


class CanBus(object):
  def __init__(self):
    self.gateway = 0
    self.extended = 1

class CarInterface(object):
  def __init__(self, CP, sendcan=None):
    self.CP = CP

    self.frame = 0
    self.can_invalid_count = 0
    self.acc_active_prev = 0

    # *** init the major players ***
    canbus = CanBus()
    self.CS = CarState(CP, canbus)
    self.VM = VehicleModel(CP)
    self.gw_cp = get_gateway_can_parser(CP, canbus)
    self.ex_cp = get_extended_can_parser(CP, canbus)

    # sending if read only is False
    if sendcan is not None:
      self.sendcan = sendcan
      self.CC = CarController(canbus, CP.carFingerprint)


  @staticmethod
  def compute_gb(accel, speed):
    return float(accel) / 4.0

  @staticmethod
  def calc_accel_override(a_ego, a_target, v_ego, v_target):
    return 1.0

  @staticmethod
  def get_params(candidate, fingerprint):
    ret = car.CarParams.new_message()

    ret.carName = "vw"
    ret.carFingerprint = candidate

    ret.enableCruise = True

    # Disable this alert on dev branch where it duplicates and obscures the engineering UI
    ret.steerLimitAlert = False

    # TODO: gate this on detection
    ret.enableCamera = True
    std_cargo = 136

    # TODO: Remove these when converting to chassisdata.py VIN detection
    if candidate == CAR.GOLF:
      ret.mass = 1372 + std_cargo
      ret.wheelbase = 2.64
      ret.centerToFront = ret.wheelbase * 0.5

      ret.steerRatio = 14
      ret.steerActuatorDelay = 0.05
      ret.steerRateCost = 0.5
      ret.steerKf = 0.00006
      ret.steerKiBP, ret.steerKpBP = [[0.], [0.]] # m/s
      ret.steerKpV, ret.steerKiV = [[0.50], [0.25]]
      ret.steerMaxBP = [0.] # m/s
      ret.steerMaxV = [1.]

    if candidate == CAR.ATLAS:
      ret.mass = 2042 + std_cargo
      ret.wheelbase = 2.98
      ret.centerToFront = ret.wheelbase * 0.5

      ret.steerRatio = 14
      ret.steerActuatorDelay = 0.05
      ret.steerRateCost = 0.5
      ret.steerKf = 0.00006
      ret.steerKiBP, ret.steerKpBP = [[0.], [0.]] # m/s
      ret.steerKpV, ret.steerKiV = [[0.25], [0.125]]
      ret.steerMaxBP = [0.] # m/s
      ret.steerMaxV = [1.]
      ret.minSteerSpeed = 2.5 # m/s

    if candidate == CAR.OCTAVIA:
      ret.mass = 1360 + std_cargo
      ret.wheelbase = 2.69
      ret.centerToFront = ret.wheelbase * 0.5

      ret.steerRatio = 14
      ret.steerActuatorDelay = 0.1
      ret.steerRateCost = 0.5
      ret.steerKf = 0.00006
      ret.steerKiBP, ret.steerKpBP = [[0.], [0.]] # m/s
      ret.steerKpV, ret.steerKiV = [[0.375], [0.1]]
      ret.steerMaxBP = [0.] # m/s
      ret.steerMaxV = [1.]

    ret.safetyModel = car.CarParams.SafetyModels.vw
    ret.steerControlType = car.CarParams.SteerControlType.torque
    ret.steerRatioRear = 0.

    # FIXME: from gm
    # Testing removal of unused longitudinal stuffs
    ret.gasMaxBP = [0.]
    ret.gasMaxV = [.5]
    ret.brakeMaxBP = [0.]
    ret.brakeMaxV = [1.]

    ret.longPidDeadzoneBP = [0.]
    ret.longPidDeadzoneV = [0.]

    ret.longitudinalKpBP = [5., 35.]
    ret.longitudinalKpV = [2.4, 1.5]
    ret.longitudinalKiBP = [0.]
    ret.longitudinalKiV = [0.36]

    ret.stoppingControl = True
    ret.startAccel = 0.8

    # hardcoding honda civic 2016 touring params so they can be used to
    # scale unknown params for other cars
    mass_civic = 2923./2.205 + std_cargo
    wheelbase_civic = 2.70
    centerToFront_civic = wheelbase_civic * 0.4
    centerToRear_civic = wheelbase_civic - centerToFront_civic
    rotationalInertia_civic = 2500
    tireStiffnessFront_civic = 192150
    tireStiffnessRear_civic = 202500
    centerToRear = ret.wheelbase - ret.centerToFront
    # TODO: get actual value, for now starting with reasonable value for
    # civic and scaling by mass and wheelbase
    ret.rotationalInertia = rotationalInertia_civic * \
                            ret.mass * ret.wheelbase**2 / (mass_civic * wheelbase_civic**2)

    # TODO: start from empirically derived lateral slip stiffness for the civic and scale by
    # mass and CG position, so all cars will have approximately similar dyn behaviors
    ret.tireStiffnessFront = tireStiffnessFront_civic * \
                             ret.mass / mass_civic * \
                             (centerToRear / ret.wheelbase) / (centerToRear_civic / wheelbase_civic)
    ret.tireStiffnessRear = tireStiffnessRear_civic * \
                            ret.mass / mass_civic * \
                            (ret.centerToFront / ret.wheelbase) / (centerToFront_civic / wheelbase_civic)

    return ret

  # returns a car.CarState
  def update(self, c):
    canMonoTimes = []

    params = Params()

    self.gw_cp.update(int(sec_since_boot() * 1e9), False)
    self.ex_cp.update(int(sec_since_boot() * 1e9), False)
    self.CS.update(self.gw_cp, self.ex_cp)

    # create message
    ret = car.CarState.new_message()

    # speeds
    ret.vEgo = self.CS.v_ego
    ret.aEgo = self.CS.a_ego
    ret.vEgoRaw = self.CS.v_ego_raw
    ret.yawRate = self.VM.yaw_rate(self.CS.angle_steers * CV.DEG_TO_RAD, self.CS.v_ego)
    ret.standstill = self.CS.standstill
    ret.wheelSpeeds.fl = self.CS.v_wheel_fl
    ret.wheelSpeeds.fr = self.CS.v_wheel_fr
    ret.wheelSpeeds.rl = self.CS.v_wheel_rl
    ret.wheelSpeeds.rr = self.CS.v_wheel_rr

    # steering wheel
    ret.steeringAngle = self.CS.angle_steers
    ret.steeringRate = self.CS.angle_steers_rate

    # torque and user override. Driver awareness
    # timer resets when the user uses the steering wheel.
    ret.steeringPressed = self.CS.steer_override
    ret.steeringTorque = self.CS.steer_torque_driver

    # ACC cruise state
    ret.cruiseState.available = bool(self.CS.acc_enabled)
    ret.cruiseState.enabled = bool(self.CS.acc_active)
    if ret.cruiseState.enabled:
      ret.cruiseState.speed = self.CS.cruise_set_speed
    else:
      ret.cruiseState.speed = 0

    # Blinker updates
    ret.leftBlinker = bool(self.CS.left_blinker_on)
    ret.rightBlinker = bool(self.CS.right_blinker_on)

    # doors open, seatbelt unfastened
    ret.doorOpen = not self.CS.door_all_closed
    ret.seatbeltUnlatched = not self.CS.seatbelt

    # Gas, brakes and shifting
    ret.gas = self.CS.pedal_gas / 100
    ret.gasPressed = self.CS.pedal_gas > 0
    ret.brake = self.CS.user_brake / 250 # FIXME: approximated, verify
    ret.brakePressed = bool(self.CS.brake_pressed)
    ret.brakeLights = bool(self.CS.brake_lights)
    ret.gearShifter = self.CS.gear_shifter

    # Obey vehicle setting for metric, update configuration DB if there is a mismatch
    # FIXME: we don't really need to be doing this at 100hz
    is_metric = params.get("IsMetric") == "1"
    if(is_metric != self.CS.is_metric):
      params.put("IsMetric", "1" if self.CS.is_metric == 1 else "0")

    buttonEvents = []

    # blinkers
    if self.CS.left_blinker_on != self.CS.prev_left_blinker_on:
      be = car.CarState.ButtonEvent.new_message()
      be.type = 'leftBlinker'
      be.pressed = bool(self.CS.left_blinker_on)
      buttonEvents.append(be)

    if self.CS.right_blinker_on != self.CS.prev_right_blinker_on:
      be = car.CarState.ButtonEvent.new_message()
      be.type = 'rightBlinker'
      be.pressed = bool(self.CS.right_blinker_on)
      buttonEvents.append(be)

    events = []
    if not self.CS.can_valid:
      self.can_invalid_count += 1
      if self.can_invalid_count >= 5:
        events.append(create_event('commIssue', [ET.NO_ENTRY, ET.IMMEDIATE_DISABLE]))
    else:
      self.can_invalid_count = 0

    if self.CS.acc_active and not self.acc_active_prev:
      events.append(create_event('pcmEnable', [ET.ENABLE]))
    if not self.CS.acc_active:
      events.append(create_event('pcmDisable', [ET.USER_DISABLE]))

    # handle button presses
    for b in ret.buttonEvents:
      # do enable on both accel and decel buttons
      if b.type in ["accelCruise", "decelCruise"] and not b.pressed:
        events.append(create_event('buttonEnable', [ET.ENABLE]))
      # do disable on button down
      if b.type == "cancel" and b.pressed:
        events.append(create_event('buttonCancel', [ET.USER_DISABLE]))

    # TODO: JY events in progress
    if not ret.gearShifter == 'drive':
      events.append(create_event('wrongGear', [ET.NO_ENTRY, ET.SOFT_DISABLE]))
    if ret.doorOpen:
      events.append(create_event('doorOpen', [ET.NO_ENTRY, ET.SOFT_DISABLE]))
    if ret.gearShifter == 'reverse':
      events.append(create_event('reverseGear', [ET.NO_ENTRY, ET.IMMEDIATE_DISABLE]))
    if ret.gasPressed:
      events.append(create_event('pedalPressed', [ET.PRE_ENABLE]))
    if ret.seatbeltUnlatched:
      events.append(create_event('seatbeltNotLatched', [ET.NO_ENTRY, ET.SOFT_DISABLE]))
    if self.CS.esp_disabled:
      events.append(create_event('espDisabled', [ET.NO_ENTRY, ET.SOFT_DISABLE]))
    if self.CS.park_brake:
      events.append(create_event('parkBrake', [ET.NO_ENTRY, ET.USER_DISABLE]))

    if self.CS.steer_error:
      # Steering rack is not configured for Heading Control Assist, or there
      # has been a timeout or other error in its reception of HCA messages.
      events.append(create_event('steerUnavailable', [ET.NO_ENTRY, ET.IMMEDIATE_DISABLE]))


    # TODO: Enable these Comma strict safety inputs once we support ACC cancel
    #if (ret.gasPressed and not self.gas_pressed_prev) or \
    #   (ret.brakePressed and (not self.brake_pressed_prev or ret.vEgo > 0.001)):
    #  events.append(create_event('pedalPressed', [ET.NO_ENTRY, ET.USER_DISABLE]))
    #if ret.gasPressed:
    #  events.append(create_event('pedalPressed', [ET.PRE_ENABLE]))

    ret.events = events
    ret.canMonoTimes = canMonoTimes

    # update previous brake/gas pressed
    self.acc_active_prev = self.CS.acc_active

    # cast to reader so it can't be modified
    return ret.as_reader()

  def apply(self, c, perception_state=log.Live20Data.new_message()):
    self.CC.update(self.sendcan, c.enabled, self.CS, self.frame, c.actuators,
                   c.hudControl.visualAlert,
                   c.hudControl.audibleAlert,
                   c.hudControl.leftLaneVisible,
                   c.hudControl.rightLaneVisible)
    self.frame += 1
