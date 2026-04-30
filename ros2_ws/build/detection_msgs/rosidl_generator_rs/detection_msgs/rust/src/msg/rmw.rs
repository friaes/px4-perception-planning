#[cfg(feature = "serde")]
use serde::{Deserialize, Serialize};


#[link(name = "detection_msgs__rosidl_typesupport_c")]
extern "C" {
    fn rosidl_typesupport_c__get_message_type_support_handle__detection_msgs__msg__Detection2D() -> *const std::ffi::c_void;
}

#[link(name = "detection_msgs__rosidl_generator_c")]
extern "C" {
    fn detection_msgs__msg__Detection2D__init(msg: *mut Detection2D) -> bool;
    fn detection_msgs__msg__Detection2D__Sequence__init(seq: *mut rosidl_runtime_rs::Sequence<Detection2D>, size: usize) -> bool;
    fn detection_msgs__msg__Detection2D__Sequence__fini(seq: *mut rosidl_runtime_rs::Sequence<Detection2D>);
    fn detection_msgs__msg__Detection2D__Sequence__copy(in_seq: &rosidl_runtime_rs::Sequence<Detection2D>, out_seq: *mut rosidl_runtime_rs::Sequence<Detection2D>) -> bool;
}

// Corresponds to detection_msgs__msg__Detection2D
#[cfg_attr(feature = "serde", derive(Deserialize, Serialize))]

/// Bounding box

#[repr(C)]
#[derive(Clone, Debug, PartialEq, PartialOrd)]
pub struct Detection2D {

    // This member is not documented.
    #[allow(missing_docs)]
    pub x_min: f32,


    // This member is not documented.
    #[allow(missing_docs)]
    pub y_min: f32,


    // This member is not documented.
    #[allow(missing_docs)]
    pub x_max: f32,


    // This member is not documented.
    #[allow(missing_docs)]
    pub y_max: f32,

    /// Detected class label
    pub class_name: rosidl_runtime_rs::String,

    /// Class index
    pub class_id: i32,

    /// Confidence score
    pub confidence: f32,

}



impl Default for Detection2D {
  fn default() -> Self {
    unsafe {
      let mut msg = std::mem::zeroed();
      if !detection_msgs__msg__Detection2D__init(&mut msg as *mut _) {
        panic!("Call to detection_msgs__msg__Detection2D__init() failed");
      }
      msg
    }
  }
}

impl rosidl_runtime_rs::SequenceAlloc for Detection2D {
  fn sequence_init(seq: &mut rosidl_runtime_rs::Sequence<Self>, size: usize) -> bool {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { detection_msgs__msg__Detection2D__Sequence__init(seq as *mut _, size) }
  }
  fn sequence_fini(seq: &mut rosidl_runtime_rs::Sequence<Self>) {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { detection_msgs__msg__Detection2D__Sequence__fini(seq as *mut _) }
  }
  fn sequence_copy(in_seq: &rosidl_runtime_rs::Sequence<Self>, out_seq: &mut rosidl_runtime_rs::Sequence<Self>) -> bool {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { detection_msgs__msg__Detection2D__Sequence__copy(in_seq, out_seq as *mut _) }
  }
}

impl rosidl_runtime_rs::Message for Detection2D {
  type RmwMsg = Self;
  fn into_rmw_message(msg_cow: std::borrow::Cow<'_, Self>) -> std::borrow::Cow<'_, Self::RmwMsg> { msg_cow }
  fn from_rmw_message(msg: Self::RmwMsg) -> Self { msg }
}

impl rosidl_runtime_rs::RmwMessage for Detection2D where Self: Sized {
  const TYPE_NAME: &'static str = "detection_msgs/msg/Detection2D";
  fn get_type_support() -> *const std::ffi::c_void {
    // SAFETY: No preconditions for this function.
    unsafe { rosidl_typesupport_c__get_message_type_support_handle__detection_msgs__msg__Detection2D() }
  }
}


#[link(name = "detection_msgs__rosidl_typesupport_c")]
extern "C" {
    fn rosidl_typesupport_c__get_message_type_support_handle__detection_msgs__msg__Detection2DArray() -> *const std::ffi::c_void;
}

#[link(name = "detection_msgs__rosidl_generator_c")]
extern "C" {
    fn detection_msgs__msg__Detection2DArray__init(msg: *mut Detection2DArray) -> bool;
    fn detection_msgs__msg__Detection2DArray__Sequence__init(seq: *mut rosidl_runtime_rs::Sequence<Detection2DArray>, size: usize) -> bool;
    fn detection_msgs__msg__Detection2DArray__Sequence__fini(seq: *mut rosidl_runtime_rs::Sequence<Detection2DArray>);
    fn detection_msgs__msg__Detection2DArray__Sequence__copy(in_seq: &rosidl_runtime_rs::Sequence<Detection2DArray>, out_seq: *mut rosidl_runtime_rs::Sequence<Detection2DArray>) -> bool;
}

// Corresponds to detection_msgs__msg__Detection2DArray
#[cfg_attr(feature = "serde", derive(Deserialize, Serialize))]

/// Header with timestamp and frame_id

#[repr(C)]
#[derive(Clone, Debug, PartialEq, PartialOrd)]
pub struct Detection2DArray {

    // This member is not documented.
    #[allow(missing_docs)]
    pub header: std_msgs::msg::rmw::Header,

    /// Array of detections for this frame
    pub detections: rosidl_runtime_rs::Sequence<super::super::msg::rmw::Detection2D>,

    /// Performance metrics
    /// time taken for YOLO inference only
    pub inference_latency_ms: f32,

    /// time from image received to message published
    pub total_latency_ms: f32,

    /// frames per second (rolling average)
    pub fps: f32,

}



impl Default for Detection2DArray {
  fn default() -> Self {
    unsafe {
      let mut msg = std::mem::zeroed();
      if !detection_msgs__msg__Detection2DArray__init(&mut msg as *mut _) {
        panic!("Call to detection_msgs__msg__Detection2DArray__init() failed");
      }
      msg
    }
  }
}

impl rosidl_runtime_rs::SequenceAlloc for Detection2DArray {
  fn sequence_init(seq: &mut rosidl_runtime_rs::Sequence<Self>, size: usize) -> bool {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { detection_msgs__msg__Detection2DArray__Sequence__init(seq as *mut _, size) }
  }
  fn sequence_fini(seq: &mut rosidl_runtime_rs::Sequence<Self>) {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { detection_msgs__msg__Detection2DArray__Sequence__fini(seq as *mut _) }
  }
  fn sequence_copy(in_seq: &rosidl_runtime_rs::Sequence<Self>, out_seq: &mut rosidl_runtime_rs::Sequence<Self>) -> bool {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { detection_msgs__msg__Detection2DArray__Sequence__copy(in_seq, out_seq as *mut _) }
  }
}

impl rosidl_runtime_rs::Message for Detection2DArray {
  type RmwMsg = Self;
  fn into_rmw_message(msg_cow: std::borrow::Cow<'_, Self>) -> std::borrow::Cow<'_, Self::RmwMsg> { msg_cow }
  fn from_rmw_message(msg: Self::RmwMsg) -> Self { msg }
}

impl rosidl_runtime_rs::RmwMessage for Detection2DArray where Self: Sized {
  const TYPE_NAME: &'static str = "detection_msgs/msg/Detection2DArray";
  fn get_type_support() -> *const std::ffi::c_void {
    // SAFETY: No preconditions for this function.
    unsafe { rosidl_typesupport_c__get_message_type_support_handle__detection_msgs__msg__Detection2DArray() }
  }
}


