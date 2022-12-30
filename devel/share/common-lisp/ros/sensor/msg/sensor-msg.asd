
(cl:in-package :asdf)

(defsystem "sensor-msg"
  :depends-on (:roslisp-msg-protocol :roslisp-utils :nav_msgs-msg
               :sensor_msgs-msg
               :std_msgs-msg
)
  :components ((:file "_package")
    (:file "CombinedSensor" :depends-on ("_package_CombinedSensor"))
    (:file "_package_CombinedSensor" :depends-on ("_package"))
  ))