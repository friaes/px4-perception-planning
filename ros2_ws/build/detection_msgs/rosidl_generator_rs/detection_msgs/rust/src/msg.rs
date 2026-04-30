#[cfg(feature = "serde")]
use serde::{Deserialize, Serialize};



// Corresponds to detection_msgs__msg__Detection2D
/// Bounding box

#[cfg_attr(feature = "serde", derive(Deserialize, Serialize))]
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
    pub class_name: std::string::String,

    /// Class index
    pub class_id: i32,

    /// Confidence score
    pub confidence: f32,

}



impl Default for Detection2D {
  fn default() -> Self {
    <Self as rosidl_runtime_rs::Message>::from_rmw_message(super::msg::rmw::Detection2D::default())
  }
}

impl rosidl_runtime_rs::Message for Detection2D {
  type RmwMsg = super::msg::rmw::Detection2D;

  fn into_rmw_message(msg_cow: std::borrow::Cow<'_, Self>) -> std::borrow::Cow<'_, Self::RmwMsg> {
    match msg_cow {
      std::borrow::Cow::Owned(msg) => std::borrow::Cow::Owned(Self::RmwMsg {
        x_min: msg.x_min,
        y_min: msg.y_min,
        x_max: msg.x_max,
        y_max: msg.y_max,
        class_name: msg.class_name.as_str().into(),
        class_id: msg.class_id,
        confidence: msg.confidence,
      }),
      std::borrow::Cow::Borrowed(msg) => std::borrow::Cow::Owned(Self::RmwMsg {
      x_min: msg.x_min,
      y_min: msg.y_min,
      x_max: msg.x_max,
      y_max: msg.y_max,
        class_name: msg.class_name.as_str().into(),
      class_id: msg.class_id,
      confidence: msg.confidence,
      })
    }
  }

  fn from_rmw_message(msg: Self::RmwMsg) -> Self {
    Self {
      x_min: msg.x_min,
      y_min: msg.y_min,
      x_max: msg.x_max,
      y_max: msg.y_max,
      class_name: msg.class_name.to_string(),
      class_id: msg.class_id,
      confidence: msg.confidence,
    }
  }
}


// Corresponds to detection_msgs__msg__Detection2DArray
/// Header with timestamp and frame_id

#[cfg_attr(feature = "serde", derive(Deserialize, Serialize))]
#[derive(Clone, Debug, PartialEq, PartialOrd)]
pub struct Detection2DArray {

    // This member is not documented.
    #[allow(missing_docs)]
    pub header: std_msgs::msg::Header,

    /// Array of detections for this frame
    pub detections: Vec<super::msg::Detection2D>,

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
    <Self as rosidl_runtime_rs::Message>::from_rmw_message(super::msg::rmw::Detection2DArray::default())
  }
}

impl rosidl_runtime_rs::Message for Detection2DArray {
  type RmwMsg = super::msg::rmw::Detection2DArray;

  fn into_rmw_message(msg_cow: std::borrow::Cow<'_, Self>) -> std::borrow::Cow<'_, Self::RmwMsg> {
    match msg_cow {
      std::borrow::Cow::Owned(msg) => std::borrow::Cow::Owned(Self::RmwMsg {
        header: std_msgs::msg::Header::into_rmw_message(std::borrow::Cow::Owned(msg.header)).into_owned(),
        detections: msg.detections
          .into_iter()
          .map(|elem| super::msg::Detection2D::into_rmw_message(std::borrow::Cow::Owned(elem)).into_owned())
          .collect(),
        inference_latency_ms: msg.inference_latency_ms,
        total_latency_ms: msg.total_latency_ms,
        fps: msg.fps,
      }),
      std::borrow::Cow::Borrowed(msg) => std::borrow::Cow::Owned(Self::RmwMsg {
        header: std_msgs::msg::Header::into_rmw_message(std::borrow::Cow::Borrowed(&msg.header)).into_owned(),
        detections: msg.detections
          .iter()
          .map(|elem| super::msg::Detection2D::into_rmw_message(std::borrow::Cow::Borrowed(elem)).into_owned())
          .collect(),
      inference_latency_ms: msg.inference_latency_ms,
      total_latency_ms: msg.total_latency_ms,
      fps: msg.fps,
      })
    }
  }

  fn from_rmw_message(msg: Self::RmwMsg) -> Self {
    Self {
      header: std_msgs::msg::Header::from_rmw_message(msg.header),
      detections: msg.detections
          .into_iter()
          .map(super::msg::Detection2D::from_rmw_message)
          .collect(),
      inference_latency_ms: msg.inference_latency_ms,
      total_latency_ms: msg.total_latency_ms,
      fps: msg.fps,
    }
  }
}


