// generated from rosidl_generator_c/resource/idl__description.c.em
// with input from detection_msgs:msg/Detection2DArray.idl
// generated code does not contain a copyright notice

#include "detection_msgs/msg/detail/detection2_d_array__functions.h"

ROSIDL_GENERATOR_C_PUBLIC_detection_msgs
const rosidl_type_hash_t *
detection_msgs__msg__Detection2DArray__get_type_hash(
  const rosidl_message_type_support_t * type_support)
{
  (void)type_support;
  static rosidl_type_hash_t hash = {1, {
      0xaf, 0x8c, 0x55, 0x7b, 0xba, 0xaa, 0xf4, 0xa9,
      0xa8, 0x56, 0x2e, 0xa3, 0xaa, 0xee, 0xeb, 0x70,
      0xe3, 0x22, 0x2c, 0x35, 0x90, 0x6c, 0x47, 0x91,
      0x0a, 0x41, 0x77, 0x13, 0xb8, 0x96, 0x5b, 0x98,
    }};
  return &hash;
}

#include <assert.h>
#include <string.h>

// Include directives for referenced types
#include "builtin_interfaces/msg/detail/time__functions.h"
#include "detection_msgs/msg/detail/detection2_d__functions.h"
#include "std_msgs/msg/detail/header__functions.h"

// Hashes for external referenced types
#ifndef NDEBUG
static const rosidl_type_hash_t builtin_interfaces__msg__Time__EXPECTED_HASH = {1, {
    0xb1, 0x06, 0x23, 0x5e, 0x25, 0xa4, 0xc5, 0xed,
    0x35, 0x09, 0x8a, 0xa0, 0xa6, 0x1a, 0x3e, 0xe9,
    0xc9, 0xb1, 0x8d, 0x19, 0x7f, 0x39, 0x8b, 0x0e,
    0x42, 0x06, 0xce, 0xa9, 0xac, 0xf9, 0xc1, 0x97,
  }};
static const rosidl_type_hash_t detection_msgs__msg__Detection2D__EXPECTED_HASH = {1, {
    0xcb, 0x08, 0x1f, 0x8f, 0xd7, 0xf8, 0x2f, 0xe3,
    0xa9, 0x0d, 0xc8, 0x09, 0xc8, 0x15, 0xdc, 0xca,
    0x6d, 0x3e, 0x0f, 0xc4, 0x5e, 0x16, 0x24, 0x0c,
    0x12, 0x4a, 0x07, 0x50, 0x17, 0x96, 0x89, 0x93,
  }};
static const rosidl_type_hash_t std_msgs__msg__Header__EXPECTED_HASH = {1, {
    0xf4, 0x9f, 0xb3, 0xae, 0x2c, 0xf0, 0x70, 0xf7,
    0x93, 0x64, 0x5f, 0xf7, 0x49, 0x68, 0x3a, 0xc6,
    0xb0, 0x62, 0x03, 0xe4, 0x1c, 0x89, 0x1e, 0x17,
    0x70, 0x1b, 0x1c, 0xb5, 0x97, 0xce, 0x6a, 0x01,
  }};
#endif

static char detection_msgs__msg__Detection2DArray__TYPE_NAME[] = "detection_msgs/msg/Detection2DArray";
static char builtin_interfaces__msg__Time__TYPE_NAME[] = "builtin_interfaces/msg/Time";
static char detection_msgs__msg__Detection2D__TYPE_NAME[] = "detection_msgs/msg/Detection2D";
static char std_msgs__msg__Header__TYPE_NAME[] = "std_msgs/msg/Header";

// Define type names, field names, and default values
static char detection_msgs__msg__Detection2DArray__FIELD_NAME__header[] = "header";
static char detection_msgs__msg__Detection2DArray__FIELD_NAME__detections[] = "detections";
static char detection_msgs__msg__Detection2DArray__FIELD_NAME__inference_latency_ms[] = "inference_latency_ms";
static char detection_msgs__msg__Detection2DArray__FIELD_NAME__total_latency_ms[] = "total_latency_ms";
static char detection_msgs__msg__Detection2DArray__FIELD_NAME__fps[] = "fps";

static rosidl_runtime_c__type_description__Field detection_msgs__msg__Detection2DArray__FIELDS[] = {
  {
    {detection_msgs__msg__Detection2DArray__FIELD_NAME__header, 6, 6},
    {
      rosidl_runtime_c__type_description__FieldType__FIELD_TYPE_NESTED_TYPE,
      0,
      0,
      {std_msgs__msg__Header__TYPE_NAME, 19, 19},
    },
    {NULL, 0, 0},
  },
  {
    {detection_msgs__msg__Detection2DArray__FIELD_NAME__detections, 10, 10},
    {
      rosidl_runtime_c__type_description__FieldType__FIELD_TYPE_NESTED_TYPE_UNBOUNDED_SEQUENCE,
      0,
      0,
      {detection_msgs__msg__Detection2D__TYPE_NAME, 30, 30},
    },
    {NULL, 0, 0},
  },
  {
    {detection_msgs__msg__Detection2DArray__FIELD_NAME__inference_latency_ms, 20, 20},
    {
      rosidl_runtime_c__type_description__FieldType__FIELD_TYPE_FLOAT,
      0,
      0,
      {NULL, 0, 0},
    },
    {NULL, 0, 0},
  },
  {
    {detection_msgs__msg__Detection2DArray__FIELD_NAME__total_latency_ms, 16, 16},
    {
      rosidl_runtime_c__type_description__FieldType__FIELD_TYPE_FLOAT,
      0,
      0,
      {NULL, 0, 0},
    },
    {NULL, 0, 0},
  },
  {
    {detection_msgs__msg__Detection2DArray__FIELD_NAME__fps, 3, 3},
    {
      rosidl_runtime_c__type_description__FieldType__FIELD_TYPE_FLOAT,
      0,
      0,
      {NULL, 0, 0},
    },
    {NULL, 0, 0},
  },
};

static rosidl_runtime_c__type_description__IndividualTypeDescription detection_msgs__msg__Detection2DArray__REFERENCED_TYPE_DESCRIPTIONS[] = {
  {
    {builtin_interfaces__msg__Time__TYPE_NAME, 27, 27},
    {NULL, 0, 0},
  },
  {
    {detection_msgs__msg__Detection2D__TYPE_NAME, 30, 30},
    {NULL, 0, 0},
  },
  {
    {std_msgs__msg__Header__TYPE_NAME, 19, 19},
    {NULL, 0, 0},
  },
};

const rosidl_runtime_c__type_description__TypeDescription *
detection_msgs__msg__Detection2DArray__get_type_description(
  const rosidl_message_type_support_t * type_support)
{
  (void)type_support;
  static bool constructed = false;
  static const rosidl_runtime_c__type_description__TypeDescription description = {
    {
      {detection_msgs__msg__Detection2DArray__TYPE_NAME, 35, 35},
      {detection_msgs__msg__Detection2DArray__FIELDS, 5, 5},
    },
    {detection_msgs__msg__Detection2DArray__REFERENCED_TYPE_DESCRIPTIONS, 3, 3},
  };
  if (!constructed) {
    assert(0 == memcmp(&builtin_interfaces__msg__Time__EXPECTED_HASH, builtin_interfaces__msg__Time__get_type_hash(NULL), sizeof(rosidl_type_hash_t)));
    description.referenced_type_descriptions.data[0].fields = builtin_interfaces__msg__Time__get_type_description(NULL)->type_description.fields;
    assert(0 == memcmp(&detection_msgs__msg__Detection2D__EXPECTED_HASH, detection_msgs__msg__Detection2D__get_type_hash(NULL), sizeof(rosidl_type_hash_t)));
    description.referenced_type_descriptions.data[1].fields = detection_msgs__msg__Detection2D__get_type_description(NULL)->type_description.fields;
    assert(0 == memcmp(&std_msgs__msg__Header__EXPECTED_HASH, std_msgs__msg__Header__get_type_hash(NULL), sizeof(rosidl_type_hash_t)));
    description.referenced_type_descriptions.data[2].fields = std_msgs__msg__Header__get_type_description(NULL)->type_description.fields;
    constructed = true;
  }
  return &description;
}

static char toplevel_type_raw_source[] =
  "# Header with timestamp and frame_id\n"
  "std_msgs/Header header\n"
  "\n"
  "# Array of detections for this frame\n"
  "Detection2D[] detections\n"
  "\n"
  "# Performance metrics\n"
  "float32 inference_latency_ms   # time taken for YOLO inference only\n"
  "float32 total_latency_ms       # time from image received to message published\n"
  "float32 fps                    # frames per second (rolling average)";

static char msg_encoding[] = "msg";

// Define all individual source functions

const rosidl_runtime_c__type_description__TypeSource *
detection_msgs__msg__Detection2DArray__get_individual_type_description_source(
  const rosidl_message_type_support_t * type_support)
{
  (void)type_support;
  static const rosidl_runtime_c__type_description__TypeSource source = {
    {detection_msgs__msg__Detection2DArray__TYPE_NAME, 35, 35},
    {msg_encoding, 3, 3},
    {toplevel_type_raw_source, 362, 362},
  };
  return &source;
}

const rosidl_runtime_c__type_description__TypeSource__Sequence *
detection_msgs__msg__Detection2DArray__get_type_description_sources(
  const rosidl_message_type_support_t * type_support)
{
  (void)type_support;
  static rosidl_runtime_c__type_description__TypeSource sources[4];
  static const rosidl_runtime_c__type_description__TypeSource__Sequence source_sequence = {sources, 4, 4};
  static bool constructed = false;
  if (!constructed) {
    sources[0] = *detection_msgs__msg__Detection2DArray__get_individual_type_description_source(NULL),
    sources[1] = *builtin_interfaces__msg__Time__get_individual_type_description_source(NULL);
    sources[2] = *detection_msgs__msg__Detection2D__get_individual_type_description_source(NULL);
    sources[3] = *std_msgs__msg__Header__get_individual_type_description_source(NULL);
    constructed = true;
  }
  return &source_sequence;
}
