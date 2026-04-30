// generated from rosidl_generator_c/resource/idl__description.c.em
// with input from detection_msgs:msg/Detection2D.idl
// generated code does not contain a copyright notice

#include "detection_msgs/msg/detail/detection2_d__functions.h"

ROSIDL_GENERATOR_C_PUBLIC_detection_msgs
const rosidl_type_hash_t *
detection_msgs__msg__Detection2D__get_type_hash(
  const rosidl_message_type_support_t * type_support)
{
  (void)type_support;
  static rosidl_type_hash_t hash = {1, {
      0xcb, 0x08, 0x1f, 0x8f, 0xd7, 0xf8, 0x2f, 0xe3,
      0xa9, 0x0d, 0xc8, 0x09, 0xc8, 0x15, 0xdc, 0xca,
      0x6d, 0x3e, 0x0f, 0xc4, 0x5e, 0x16, 0x24, 0x0c,
      0x12, 0x4a, 0x07, 0x50, 0x17, 0x96, 0x89, 0x93,
    }};
  return &hash;
}

#include <assert.h>
#include <string.h>

// Include directives for referenced types

// Hashes for external referenced types
#ifndef NDEBUG
#endif

static char detection_msgs__msg__Detection2D__TYPE_NAME[] = "detection_msgs/msg/Detection2D";

// Define type names, field names, and default values
static char detection_msgs__msg__Detection2D__FIELD_NAME__x_min[] = "x_min";
static char detection_msgs__msg__Detection2D__FIELD_NAME__y_min[] = "y_min";
static char detection_msgs__msg__Detection2D__FIELD_NAME__x_max[] = "x_max";
static char detection_msgs__msg__Detection2D__FIELD_NAME__y_max[] = "y_max";
static char detection_msgs__msg__Detection2D__FIELD_NAME__class_name[] = "class_name";
static char detection_msgs__msg__Detection2D__FIELD_NAME__class_id[] = "class_id";
static char detection_msgs__msg__Detection2D__FIELD_NAME__confidence[] = "confidence";

static rosidl_runtime_c__type_description__Field detection_msgs__msg__Detection2D__FIELDS[] = {
  {
    {detection_msgs__msg__Detection2D__FIELD_NAME__x_min, 5, 5},
    {
      rosidl_runtime_c__type_description__FieldType__FIELD_TYPE_FLOAT,
      0,
      0,
      {NULL, 0, 0},
    },
    {NULL, 0, 0},
  },
  {
    {detection_msgs__msg__Detection2D__FIELD_NAME__y_min, 5, 5},
    {
      rosidl_runtime_c__type_description__FieldType__FIELD_TYPE_FLOAT,
      0,
      0,
      {NULL, 0, 0},
    },
    {NULL, 0, 0},
  },
  {
    {detection_msgs__msg__Detection2D__FIELD_NAME__x_max, 5, 5},
    {
      rosidl_runtime_c__type_description__FieldType__FIELD_TYPE_FLOAT,
      0,
      0,
      {NULL, 0, 0},
    },
    {NULL, 0, 0},
  },
  {
    {detection_msgs__msg__Detection2D__FIELD_NAME__y_max, 5, 5},
    {
      rosidl_runtime_c__type_description__FieldType__FIELD_TYPE_FLOAT,
      0,
      0,
      {NULL, 0, 0},
    },
    {NULL, 0, 0},
  },
  {
    {detection_msgs__msg__Detection2D__FIELD_NAME__class_name, 10, 10},
    {
      rosidl_runtime_c__type_description__FieldType__FIELD_TYPE_STRING,
      0,
      0,
      {NULL, 0, 0},
    },
    {NULL, 0, 0},
  },
  {
    {detection_msgs__msg__Detection2D__FIELD_NAME__class_id, 8, 8},
    {
      rosidl_runtime_c__type_description__FieldType__FIELD_TYPE_INT32,
      0,
      0,
      {NULL, 0, 0},
    },
    {NULL, 0, 0},
  },
  {
    {detection_msgs__msg__Detection2D__FIELD_NAME__confidence, 10, 10},
    {
      rosidl_runtime_c__type_description__FieldType__FIELD_TYPE_FLOAT,
      0,
      0,
      {NULL, 0, 0},
    },
    {NULL, 0, 0},
  },
};

const rosidl_runtime_c__type_description__TypeDescription *
detection_msgs__msg__Detection2D__get_type_description(
  const rosidl_message_type_support_t * type_support)
{
  (void)type_support;
  static bool constructed = false;
  static const rosidl_runtime_c__type_description__TypeDescription description = {
    {
      {detection_msgs__msg__Detection2D__TYPE_NAME, 30, 30},
      {detection_msgs__msg__Detection2D__FIELDS, 7, 7},
    },
    {NULL, 0, 0},
  };
  if (!constructed) {
    constructed = true;
  }
  return &description;
}

static char toplevel_type_raw_source[] =
  "# Bounding box\n"
  "float32 x_min\n"
  "float32 y_min\n"
  "float32 x_max\n"
  "float32 y_max\n"
  "\n"
  "# Detected class label\n"
  "string class_name\n"
  "\n"
  "# Class index\n"
  "int32 class_id\n"
  "\n"
  "# Confidence score\n"
  "float32 confidence";

static char msg_encoding[] = "msg";

// Define all individual source functions

const rosidl_runtime_c__type_description__TypeSource *
detection_msgs__msg__Detection2D__get_individual_type_description_source(
  const rosidl_message_type_support_t * type_support)
{
  (void)type_support;
  static const rosidl_runtime_c__type_description__TypeSource source = {
    {detection_msgs__msg__Detection2D__TYPE_NAME, 30, 30},
    {msg_encoding, 3, 3},
    {toplevel_type_raw_source, 182, 182},
  };
  return &source;
}

const rosidl_runtime_c__type_description__TypeSource__Sequence *
detection_msgs__msg__Detection2D__get_type_description_sources(
  const rosidl_message_type_support_t * type_support)
{
  (void)type_support;
  static rosidl_runtime_c__type_description__TypeSource sources[1];
  static const rosidl_runtime_c__type_description__TypeSource__Sequence source_sequence = {sources, 1, 1};
  static bool constructed = false;
  if (!constructed) {
    sources[0] = *detection_msgs__msg__Detection2D__get_individual_type_description_source(NULL),
    constructed = true;
  }
  return &source_sequence;
}
