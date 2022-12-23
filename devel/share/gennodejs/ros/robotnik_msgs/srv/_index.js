
"use strict";

let SetMotorPID = require('./SetMotorPID.js')
let set_height = require('./set_height.js')
let SetEncoderTurns = require('./SetEncoderTurns.js')
let axis_record = require('./axis_record.js')
let set_named_digital_output = require('./set_named_digital_output.js')
let GetPOI = require('./GetPOI.js')
let SetElevator = require('./SetElevator.js')
let set_analog_output = require('./set_analog_output.js')
let set_modbus_register = require('./set_modbus_register.js')
let SetCurrent = require('./SetCurrent.js')
let set_digital_output = require('./set_digital_output.js')
let get_digital_input = require('./get_digital_input.js')
let QueryAlarms = require('./QueryAlarms.js')
let set_odometry = require('./set_odometry.js')
let set_float_value = require('./set_float_value.js')
let GetPTZ = require('./GetPTZ.js')
let get_mode = require('./get_mode.js')
let ResetFromSubState = require('./ResetFromSubState.js')
let get_alarms = require('./get_alarms.js')
let SetInt16 = require('./SetInt16.js')
let SetTransform = require('./SetTransform.js')
let set_mode = require('./set_mode.js')
let set_CartesianEuler_pose = require('./set_CartesianEuler_pose.js')
let ack_alarm = require('./ack_alarm.js')
let enable_disable = require('./enable_disable.js')
let SetMotorMode = require('./SetMotorMode.js')
let SetLaserMode = require('./SetLaserMode.js')
let SetByte = require('./SetByte.js')
let GetMotorsHeadingOffset = require('./GetMotorsHeadingOffset.js')
let SetMotorStatus = require('./SetMotorStatus.js')
let home = require('./home.js')
let SetNamedDigitalOutput = require('./SetNamedDigitalOutput.js')
let get_modbus_register = require('./get_modbus_register.js')
let GetBool = require('./GetBool.js')
let SetBuzzer = require('./SetBuzzer.js')
let SetString = require('./SetString.js')
let InsertTask = require('./InsertTask.js')
let set_ptz = require('./set_ptz.js')

module.exports = {
  SetMotorPID: SetMotorPID,
  set_height: set_height,
  SetEncoderTurns: SetEncoderTurns,
  axis_record: axis_record,
  set_named_digital_output: set_named_digital_output,
  GetPOI: GetPOI,
  SetElevator: SetElevator,
  set_analog_output: set_analog_output,
  set_modbus_register: set_modbus_register,
  SetCurrent: SetCurrent,
  set_digital_output: set_digital_output,
  get_digital_input: get_digital_input,
  QueryAlarms: QueryAlarms,
  set_odometry: set_odometry,
  set_float_value: set_float_value,
  GetPTZ: GetPTZ,
  get_mode: get_mode,
  ResetFromSubState: ResetFromSubState,
  get_alarms: get_alarms,
  SetInt16: SetInt16,
  SetTransform: SetTransform,
  set_mode: set_mode,
  set_CartesianEuler_pose: set_CartesianEuler_pose,
  ack_alarm: ack_alarm,
  enable_disable: enable_disable,
  SetMotorMode: SetMotorMode,
  SetLaserMode: SetLaserMode,
  SetByte: SetByte,
  GetMotorsHeadingOffset: GetMotorsHeadingOffset,
  SetMotorStatus: SetMotorStatus,
  home: home,
  SetNamedDigitalOutput: SetNamedDigitalOutput,
  get_modbus_register: get_modbus_register,
  GetBool: GetBool,
  SetBuzzer: SetBuzzer,
  SetString: SetString,
  InsertTask: InsertTask,
  set_ptz: set_ptz,
};
