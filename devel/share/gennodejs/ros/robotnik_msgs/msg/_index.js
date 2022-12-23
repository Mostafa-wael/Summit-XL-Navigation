
"use strict";

let SafetyModuleStatus = require('./SafetyModuleStatus.js');
let MotorReferenceValueArray = require('./MotorReferenceValueArray.js');
let PresenceSensorArray = require('./PresenceSensorArray.js');
let SubState = require('./SubState.js');
let LaserMode = require('./LaserMode.js');
let alarmmonitor = require('./alarmmonitor.js');
let RobotnikMotorsStatus = require('./RobotnikMotorsStatus.js');
let Axis = require('./Axis.js');
let Interfaces = require('./Interfaces.js');
let encoders = require('./encoders.js');
let Cartesian_Euler_pose = require('./Cartesian_Euler_pose.js');
let ptz = require('./ptz.js');
let BatteryStatus = require('./BatteryStatus.js');
let State = require('./State.js');
let Registers = require('./Registers.js');
let BatteryStatusStamped = require('./BatteryStatusStamped.js');
let PantiltStatus = require('./PantiltStatus.js');
let QueryAlarm = require('./QueryAlarm.js');
let OdomManualCalibrationStatusStamped = require('./OdomManualCalibrationStatusStamped.js');
let BatteryDockingStatusStamped = require('./BatteryDockingStatusStamped.js');
let WatchdogStatusArray = require('./WatchdogStatusArray.js');
let StringArray = require('./StringArray.js');
let ElevatorAction = require('./ElevatorAction.js');
let ReturnMessage = require('./ReturnMessage.js');
let WatchdogStatus = require('./WatchdogStatus.js');
let Pose2DArray = require('./Pose2DArray.js');
let OdomCalibrationStatusStamped = require('./OdomCalibrationStatusStamped.js');
let Register = require('./Register.js');
let BoolArray = require('./BoolArray.js');
let MotorCurrent = require('./MotorCurrent.js');
let MotorStatus = require('./MotorStatus.js');
let MotorsStatus = require('./MotorsStatus.js');
let inputs_outputs = require('./inputs_outputs.js');
let AlarmSensor = require('./AlarmSensor.js');
let PresenceSensor = require('./PresenceSensor.js');
let ArmStatus = require('./ArmStatus.js');
let BatteryDockingStatus = require('./BatteryDockingStatus.js');
let InverterStatus = require('./InverterStatus.js');
let named_inputs_outputs = require('./named_inputs_outputs.js');
let Alarms = require('./Alarms.js');
let MotorPID = require('./MotorPID.js');
let ElevatorStatus = require('./ElevatorStatus.js');
let OdomManualCalibrationStatus = require('./OdomManualCalibrationStatus.js');
let MotorReferenceValue = require('./MotorReferenceValue.js');
let alarmsmonitor = require('./alarmsmonitor.js');
let MotorHeadingOffset = require('./MotorHeadingOffset.js');
let OdomCalibrationStatus = require('./OdomCalibrationStatus.js');
let Data = require('./Data.js');
let StringStamped = require('./StringStamped.js');
let PantiltStatusStamped = require('./PantiltStatusStamped.js');
let MotorsStatusDifferential = require('./MotorsStatusDifferential.js');
let named_input_output = require('./named_input_output.js');
let Pose2DStamped = require('./Pose2DStamped.js');
let LaserStatus = require('./LaserStatus.js');
let SetElevatorFeedback = require('./SetElevatorFeedback.js');
let SetElevatorResult = require('./SetElevatorResult.js');
let SetElevatorActionFeedback = require('./SetElevatorActionFeedback.js');
let SetElevatorAction = require('./SetElevatorAction.js');
let SetElevatorActionGoal = require('./SetElevatorActionGoal.js');
let SetElevatorGoal = require('./SetElevatorGoal.js');
let SetElevatorActionResult = require('./SetElevatorActionResult.js');

module.exports = {
  SafetyModuleStatus: SafetyModuleStatus,
  MotorReferenceValueArray: MotorReferenceValueArray,
  PresenceSensorArray: PresenceSensorArray,
  SubState: SubState,
  LaserMode: LaserMode,
  alarmmonitor: alarmmonitor,
  RobotnikMotorsStatus: RobotnikMotorsStatus,
  Axis: Axis,
  Interfaces: Interfaces,
  encoders: encoders,
  Cartesian_Euler_pose: Cartesian_Euler_pose,
  ptz: ptz,
  BatteryStatus: BatteryStatus,
  State: State,
  Registers: Registers,
  BatteryStatusStamped: BatteryStatusStamped,
  PantiltStatus: PantiltStatus,
  QueryAlarm: QueryAlarm,
  OdomManualCalibrationStatusStamped: OdomManualCalibrationStatusStamped,
  BatteryDockingStatusStamped: BatteryDockingStatusStamped,
  WatchdogStatusArray: WatchdogStatusArray,
  StringArray: StringArray,
  ElevatorAction: ElevatorAction,
  ReturnMessage: ReturnMessage,
  WatchdogStatus: WatchdogStatus,
  Pose2DArray: Pose2DArray,
  OdomCalibrationStatusStamped: OdomCalibrationStatusStamped,
  Register: Register,
  BoolArray: BoolArray,
  MotorCurrent: MotorCurrent,
  MotorStatus: MotorStatus,
  MotorsStatus: MotorsStatus,
  inputs_outputs: inputs_outputs,
  AlarmSensor: AlarmSensor,
  PresenceSensor: PresenceSensor,
  ArmStatus: ArmStatus,
  BatteryDockingStatus: BatteryDockingStatus,
  InverterStatus: InverterStatus,
  named_inputs_outputs: named_inputs_outputs,
  Alarms: Alarms,
  MotorPID: MotorPID,
  ElevatorStatus: ElevatorStatus,
  OdomManualCalibrationStatus: OdomManualCalibrationStatus,
  MotorReferenceValue: MotorReferenceValue,
  alarmsmonitor: alarmsmonitor,
  MotorHeadingOffset: MotorHeadingOffset,
  OdomCalibrationStatus: OdomCalibrationStatus,
  Data: Data,
  StringStamped: StringStamped,
  PantiltStatusStamped: PantiltStatusStamped,
  MotorsStatusDifferential: MotorsStatusDifferential,
  named_input_output: named_input_output,
  Pose2DStamped: Pose2DStamped,
  LaserStatus: LaserStatus,
  SetElevatorFeedback: SetElevatorFeedback,
  SetElevatorResult: SetElevatorResult,
  SetElevatorActionFeedback: SetElevatorActionFeedback,
  SetElevatorAction: SetElevatorAction,
  SetElevatorActionGoal: SetElevatorActionGoal,
  SetElevatorGoal: SetElevatorGoal,
  SetElevatorActionResult: SetElevatorActionResult,
};
