# State Schema

## Required Top-Level Fields

- `current_brick` (string)
- `status` (string)
- `loop_count` (integer)
- `last_gate_failed` (string or null)
- `completed_bricks` (array of strings)
- `next_action` (string)
- `last_test_run` (object)

## `last_test_run` Required Fields

- `command` (string)
- `status` (`PASS` or `FAIL`)
- `exit_code` (integer)
- `artifact` (string path)

## `last_test_run` Optional Fields

- `failed_nodeids` (array of strings)
