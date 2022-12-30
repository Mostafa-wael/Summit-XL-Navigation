; Auto-generated. Do not edit!


(cl:in-package sensor-msg)


;//! \htmlinclude sensor.msg.html

(cl:defclass <sensor> (roslisp-msg-protocol:ros-message)
  ((header
    :reader header
    :initarg :header
    :type std_msgs-msg:Header
    :initform (cl:make-instance 'std_msgs-msg:Header))
   (laser
    :reader laser
    :initarg :laser
    :type sensor_msgs-msg:LaserScan
    :initform (cl:make-instance 'sensor_msgs-msg:LaserScan))
   (odom
    :reader odom
    :initarg :odom
    :type nav_msgs-msg:Odometry
    :initform (cl:make-instance 'nav_msgs-msg:Odometry)))
)

(cl:defclass sensor (<sensor>)
  ())

(cl:defmethod cl:initialize-instance :after ((m <sensor>) cl:&rest args)
  (cl:declare (cl:ignorable args))
  (cl:unless (cl:typep m 'sensor)
    (roslisp-msg-protocol:msg-deprecation-warning "using old message class name sensor-msg:<sensor> is deprecated: use sensor-msg:sensor instead.")))

(cl:ensure-generic-function 'header-val :lambda-list '(m))
(cl:defmethod header-val ((m <sensor>))
  (roslisp-msg-protocol:msg-deprecation-warning "Using old-style slot reader sensor-msg:header-val is deprecated.  Use sensor-msg:header instead.")
  (header m))

(cl:ensure-generic-function 'laser-val :lambda-list '(m))
(cl:defmethod laser-val ((m <sensor>))
  (roslisp-msg-protocol:msg-deprecation-warning "Using old-style slot reader sensor-msg:laser-val is deprecated.  Use sensor-msg:laser instead.")
  (laser m))

(cl:ensure-generic-function 'odom-val :lambda-list '(m))
(cl:defmethod odom-val ((m <sensor>))
  (roslisp-msg-protocol:msg-deprecation-warning "Using old-style slot reader sensor-msg:odom-val is deprecated.  Use sensor-msg:odom instead.")
  (odom m))
(cl:defmethod roslisp-msg-protocol:serialize ((msg <sensor>) ostream)
  "Serializes a message object of type '<sensor>"
  (roslisp-msg-protocol:serialize (cl:slot-value msg 'header) ostream)
  (roslisp-msg-protocol:serialize (cl:slot-value msg 'laser) ostream)
  (roslisp-msg-protocol:serialize (cl:slot-value msg 'odom) ostream)
)
(cl:defmethod roslisp-msg-protocol:deserialize ((msg <sensor>) istream)
  "Deserializes a message object of type '<sensor>"
  (roslisp-msg-protocol:deserialize (cl:slot-value msg 'header) istream)
  (roslisp-msg-protocol:deserialize (cl:slot-value msg 'laser) istream)
  (roslisp-msg-protocol:deserialize (cl:slot-value msg 'odom) istream)
  msg
)
(cl:defmethod roslisp-msg-protocol:ros-datatype ((msg (cl:eql '<sensor>)))
  "Returns string type for a message object of type '<sensor>"
  "sensor/sensor")
(cl:defmethod roslisp-msg-protocol:ros-datatype ((msg (cl:eql 'sensor)))
  "Returns string type for a message object of type 'sensor"
  "sensor/sensor")
(cl:defmethod roslisp-msg-protocol:md5sum ((type (cl:eql '<sensor>)))
  "Returns md5sum for a message object of type '<sensor>"
  "f7c763e4f2e37abeaa519471b63785c2")
(cl:defmethod roslisp-msg-protocol:md5sum ((type (cl:eql 'sensor)))
  "Returns md5sum for a message object of type 'sensor"
  "f7c763e4f2e37abeaa519471b63785c2")
(cl:defmethod roslisp-msg-protocol:message-definition ((type (cl:eql '<sensor>)))
  "Returns full string definition for message of type '<sensor>"
  (cl:format cl:nil "Header header~%sensor_msgs/LaserScan laser~%nav_msgs/Odometry odom~%================================================================================~%MSG: std_msgs/Header~%# Standard metadata for higher-level stamped data types.~%# This is generally used to communicate timestamped data ~%# in a particular coordinate frame.~%# ~%# sequence ID: consecutively increasing ID ~%uint32 seq~%#Two-integer timestamp that is expressed as:~%# * stamp.sec: seconds (stamp_secs) since epoch (in Python the variable is called 'secs')~%# * stamp.nsec: nanoseconds since stamp_secs (in Python the variable is called 'nsecs')~%# time-handling sugar is provided by the client library~%time stamp~%#Frame this data is associated with~%string frame_id~%~%================================================================================~%MSG: sensor_msgs/LaserScan~%# Single scan from a planar laser range-finder~%#~%# If you have another ranging device with different behavior (e.g. a sonar~%# array), please find or create a different message, since applications~%# will make fairly laser-specific assumptions about this data~%~%Header header            # timestamp in the header is the acquisition time of ~%                         # the first ray in the scan.~%                         #~%                         # in frame frame_id, angles are measured around ~%                         # the positive Z axis (counterclockwise, if Z is up)~%                         # with zero angle being forward along the x axis~%                         ~%float32 angle_min        # start angle of the scan [rad]~%float32 angle_max        # end angle of the scan [rad]~%float32 angle_increment  # angular distance between measurements [rad]~%~%float32 time_increment   # time between measurements [seconds] - if your scanner~%                         # is moving, this will be used in interpolating position~%                         # of 3d points~%float32 scan_time        # time between scans [seconds]~%~%float32 range_min        # minimum range value [m]~%float32 range_max        # maximum range value [m]~%~%float32[] ranges         # range data [m] (Note: values < range_min or > range_max should be discarded)~%float32[] intensities    # intensity data [device-specific units].  If your~%                         # device does not provide intensities, please leave~%                         # the array empty.~%~%================================================================================~%MSG: nav_msgs/Odometry~%# This represents an estimate of a position and velocity in free space.  ~%# The pose in this message should be specified in the coordinate frame given by header.frame_id.~%# The twist in this message should be specified in the coordinate frame given by the child_frame_id~%Header header~%string child_frame_id~%geometry_msgs/PoseWithCovariance pose~%geometry_msgs/TwistWithCovariance twist~%~%================================================================================~%MSG: geometry_msgs/PoseWithCovariance~%# This represents a pose in free space with uncertainty.~%~%Pose pose~%~%# Row-major representation of the 6x6 covariance matrix~%# The orientation parameters use a fixed-axis representation.~%# In order, the parameters are:~%# (x, y, z, rotation about X axis, rotation about Y axis, rotation about Z axis)~%float64[36] covariance~%~%================================================================================~%MSG: geometry_msgs/Pose~%# A representation of pose in free space, composed of position and orientation. ~%Point position~%Quaternion orientation~%~%================================================================================~%MSG: geometry_msgs/Point~%# This contains the position of a point in free space~%float64 x~%float64 y~%float64 z~%~%================================================================================~%MSG: geometry_msgs/Quaternion~%# This represents an orientation in free space in quaternion form.~%~%float64 x~%float64 y~%float64 z~%float64 w~%~%================================================================================~%MSG: geometry_msgs/TwistWithCovariance~%# This expresses velocity in free space with uncertainty.~%~%Twist twist~%~%# Row-major representation of the 6x6 covariance matrix~%# The orientation parameters use a fixed-axis representation.~%# In order, the parameters are:~%# (x, y, z, rotation about X axis, rotation about Y axis, rotation about Z axis)~%float64[36] covariance~%~%================================================================================~%MSG: geometry_msgs/Twist~%# This expresses velocity in free space broken into its linear and angular parts.~%Vector3  linear~%Vector3  angular~%~%================================================================================~%MSG: geometry_msgs/Vector3~%# This represents a vector in free space. ~%# It is only meant to represent a direction. Therefore, it does not~%# make sense to apply a translation to it (e.g., when applying a ~%# generic rigid transformation to a Vector3, tf2 will only apply the~%# rotation). If you want your data to be translatable too, use the~%# geometry_msgs/Point message instead.~%~%float64 x~%float64 y~%float64 z~%~%"))
(cl:defmethod roslisp-msg-protocol:message-definition ((type (cl:eql 'sensor)))
  "Returns full string definition for message of type 'sensor"
  (cl:format cl:nil "Header header~%sensor_msgs/LaserScan laser~%nav_msgs/Odometry odom~%================================================================================~%MSG: std_msgs/Header~%# Standard metadata for higher-level stamped data types.~%# This is generally used to communicate timestamped data ~%# in a particular coordinate frame.~%# ~%# sequence ID: consecutively increasing ID ~%uint32 seq~%#Two-integer timestamp that is expressed as:~%# * stamp.sec: seconds (stamp_secs) since epoch (in Python the variable is called 'secs')~%# * stamp.nsec: nanoseconds since stamp_secs (in Python the variable is called 'nsecs')~%# time-handling sugar is provided by the client library~%time stamp~%#Frame this data is associated with~%string frame_id~%~%================================================================================~%MSG: sensor_msgs/LaserScan~%# Single scan from a planar laser range-finder~%#~%# If you have another ranging device with different behavior (e.g. a sonar~%# array), please find or create a different message, since applications~%# will make fairly laser-specific assumptions about this data~%~%Header header            # timestamp in the header is the acquisition time of ~%                         # the first ray in the scan.~%                         #~%                         # in frame frame_id, angles are measured around ~%                         # the positive Z axis (counterclockwise, if Z is up)~%                         # with zero angle being forward along the x axis~%                         ~%float32 angle_min        # start angle of the scan [rad]~%float32 angle_max        # end angle of the scan [rad]~%float32 angle_increment  # angular distance between measurements [rad]~%~%float32 time_increment   # time between measurements [seconds] - if your scanner~%                         # is moving, this will be used in interpolating position~%                         # of 3d points~%float32 scan_time        # time between scans [seconds]~%~%float32 range_min        # minimum range value [m]~%float32 range_max        # maximum range value [m]~%~%float32[] ranges         # range data [m] (Note: values < range_min or > range_max should be discarded)~%float32[] intensities    # intensity data [device-specific units].  If your~%                         # device does not provide intensities, please leave~%                         # the array empty.~%~%================================================================================~%MSG: nav_msgs/Odometry~%# This represents an estimate of a position and velocity in free space.  ~%# The pose in this message should be specified in the coordinate frame given by header.frame_id.~%# The twist in this message should be specified in the coordinate frame given by the child_frame_id~%Header header~%string child_frame_id~%geometry_msgs/PoseWithCovariance pose~%geometry_msgs/TwistWithCovariance twist~%~%================================================================================~%MSG: geometry_msgs/PoseWithCovariance~%# This represents a pose in free space with uncertainty.~%~%Pose pose~%~%# Row-major representation of the 6x6 covariance matrix~%# The orientation parameters use a fixed-axis representation.~%# In order, the parameters are:~%# (x, y, z, rotation about X axis, rotation about Y axis, rotation about Z axis)~%float64[36] covariance~%~%================================================================================~%MSG: geometry_msgs/Pose~%# A representation of pose in free space, composed of position and orientation. ~%Point position~%Quaternion orientation~%~%================================================================================~%MSG: geometry_msgs/Point~%# This contains the position of a point in free space~%float64 x~%float64 y~%float64 z~%~%================================================================================~%MSG: geometry_msgs/Quaternion~%# This represents an orientation in free space in quaternion form.~%~%float64 x~%float64 y~%float64 z~%float64 w~%~%================================================================================~%MSG: geometry_msgs/TwistWithCovariance~%# This expresses velocity in free space with uncertainty.~%~%Twist twist~%~%# Row-major representation of the 6x6 covariance matrix~%# The orientation parameters use a fixed-axis representation.~%# In order, the parameters are:~%# (x, y, z, rotation about X axis, rotation about Y axis, rotation about Z axis)~%float64[36] covariance~%~%================================================================================~%MSG: geometry_msgs/Twist~%# This expresses velocity in free space broken into its linear and angular parts.~%Vector3  linear~%Vector3  angular~%~%================================================================================~%MSG: geometry_msgs/Vector3~%# This represents a vector in free space. ~%# It is only meant to represent a direction. Therefore, it does not~%# make sense to apply a translation to it (e.g., when applying a ~%# generic rigid transformation to a Vector3, tf2 will only apply the~%# rotation). If you want your data to be translatable too, use the~%# geometry_msgs/Point message instead.~%~%float64 x~%float64 y~%float64 z~%~%"))
(cl:defmethod roslisp-msg-protocol:serialization-length ((msg <sensor>))
  (cl:+ 0
     (roslisp-msg-protocol:serialization-length (cl:slot-value msg 'header))
     (roslisp-msg-protocol:serialization-length (cl:slot-value msg 'laser))
     (roslisp-msg-protocol:serialization-length (cl:slot-value msg 'odom))
))
(cl:defmethod roslisp-msg-protocol:ros-message-to-list ((msg <sensor>))
  "Converts a ROS message object to a list"
  (cl:list 'sensor
    (cl:cons ':header (header msg))
    (cl:cons ':laser (laser msg))
    (cl:cons ':odom (odom msg))
))
