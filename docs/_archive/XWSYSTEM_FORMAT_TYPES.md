# XWSystem Format Types Specification

This document defines format types that should be supported in xwsystem for use with XWSchema's `format` parameter.

## Standard Format Types

These format types follow international standards and best practices for data validation and representation.

### Identity & Authentication

#### `username`
- **Type**: string
- **Format**: `username`
- **Pattern**: `^[a-zA-Z0-9][a-zA-Z0-9_.-]*[a-zA-Z0-9]$|^[a-zA-Z0-9]$`
- **Description**: Username identifier. Must start and end with alphanumeric character. Can contain letters, numbers, underscores, dots, and hyphens in between.
- **Length**: Typically 3-30 characters
- **Examples**: `john_doe`, `user123`, `alice.smith`

#### `email`
- **Type**: string
- **Format**: `email`
- **Description**: Email address following RFC 5322 (standard email format)
- **Examples**: `user@example.com`, `test+tag@domain.co.uk`

#### `password`
- **Type**: string
- **Format**: `password`
- **Confidential**: true (should never be exposed in logs or serialization)
- **Length**: Typically minimum 8 characters (configurable)
- **Description**: Password field (stored as hash, never plaintext)

#### `auth_code`
- **Type**: string
- **Format**: `auth_code`
- **Pattern**: Typically alphanumeric (e.g., `^[A-Z0-9]{6,8}$`)
- **Description**: Authentication code (2FA codes, verification codes)
- **Examples**: `123456`, `ABC123`

#### `token`
- **Type**: string
- **Format**: `token`
- **Pattern**: `^[A-Za-z0-9+/=_-]+$` (Base64-safe characters)
- **Description**: Authentication token (JWT, session tokens, API tokens)
- **Length**: Typically 32-512 characters

### Network & Location

#### `ip_address`
- **Type**: string
- **Format**: `ip-address` or `ipv4` / `ipv6`
- **Pattern IPv4**: `^(?:[0-9]{1,3}\.){3}[0-9]{1,3}$`
- **Pattern IPv6**: `^(?:[0-9a-fA-F]{0,4}:){2,7}[0-9a-fA-F]{0,4}$`
- **Description**: IP address (supports both IPv4 and IPv6)
- **Examples**: `192.168.1.1`, `2001:0db8:85a3:0000:0000:8a2e:0370:7334`

#### `url` / `uri`
- **Type**: string
- **Format**: `uri` (already supported in JSON Schema)
- **Description**: Uniform Resource Identifier (URL/URI)
- **Examples**: `https://example.com/path`, `ftp://files.example.com`

#### `location`
- **Type**: object or string
- **Format**: `location`
- **Description**: Geographic location. Can be:
  - String: Place name (e.g., "New York, NY", "London, UK")
  - Object: Structured location with coordinates
- **When object**: Should contain `longitude` and `latitude` (and optionally `altitude`)

#### `longitude`
- **Type**: number (float)
- **Format**: `longitude`
- **Range**: -180.0 to 180.0
- **Description**: Longitude coordinate (degrees)
- **Examples**: `-74.0060`, `0.1278`

#### `latitude`
- **Type**: number (float)
- **Format**: `latitude`
- **Range**: -90.0 to 90.0
- **Description**: Latitude coordinate (degrees)
- **Examples**: `40.7128`, `51.5074`

#### `altitude`
- **Type**: number (float)
- **Format**: `altitude`
- **Range**: Typically -10984 to 8848 meters (sea level ± Mount Everest range)
- **Description**: Altitude/elevation in meters above sea level
- **Examples**: `0`, `8848`, `-400`

#### `coordinates`
- **Type**: object
- **Format**: `coordinates`
- **Properties**:
  - `longitude` (required): number, -180.0 to 180.0
  - `latitude` (required): number, -90.0 to 90.0
  - `altitude` (optional): number
- **Description**: Complete coordinate set (longitude, latitude, optionally altitude)
- **Examples**: 
  ```json
  {"longitude": -74.0060, "latitude": 40.7128}
  {"longitude": 0.1278, "latitude": 51.5074, "altitude": 35}
  ```

#### `address`
- **Type**: object
- **Format**: `address`
- **Description**: Physical address following international standards (ISO 19160, UPU S42)
- **Properties** (flexible, depends on country):
  - `street` / `street_address`: string
  - `city` / `locality`: string
  - `state` / `region` / `province`: string
  - `postal_code` / `zip_code`: string
  - `country`: string (ISO 3166-1 alpha-2 code, e.g., "US", "GB")
  - `country_code`: string (ISO 3166-1 alpha-2)
- **Examples**:
  ```json
  {
    "street": "123 Main St",
    "city": "New York",
    "state": "NY",
    "postal_code": "10001",
    "country": "US"
  }
  ```

### Date & Time

#### `datetime`
- **Type**: string or datetime object
- **Format**: `date-time` (already supported in JSON Schema, ISO 8601)
- **Description**: Date and time in ISO 8601 format
- **Examples**: `2023-12-25T10:30:00Z`, `2023-12-25T10:30:00+00:00`

#### `date`
- **Type**: string or date object
- **Format**: `date` (already supported in JSON Schema, ISO 8601)
- **Description**: Date only (YYYY-MM-DD)
- **Examples**: `2023-12-25`

#### `time`
- **Type**: string or time object
- **Format**: `time` (already supported in JSON Schema, ISO 8601)
- **Description**: Time only (HH:MM:SS)
- **Examples**: `10:30:00`, `14:30:00`

### Miscellaneous

#### `color_hash`
- **Type**: string
- **Format**: `color-hash` or `color-hex`
- **Pattern**: `^#[0-9A-Fa-f]{6}$` (hex color) or `^[0-9A-Fa-f]{6}$`
- **Description**: Color represented as hexadecimal hash (HTML/CSS color codes)
- **Examples**: `#FF5733`, `#00FF00`, `FF5733`

## Usage Examples

### In XWSchema

```python
from exonware.xwschema import XWSchema
from exonware.xwentity import XWEntity
from typing import Optional

class User(XWEntity):
    @XWSchema(
        format="email",
        required=True,
        description="User email address"
    )
    def email(self) -> str: pass
    
    @XWSchema(
        format="username",
        length_min=3,
        length_max=30,
        required=True,
        description="Unique username"
    )
    def username(self) -> str: pass
    
    @XWSchema(
        format="ip-address",
        description="Last login IP address"
    )
    def last_login_ip(self) -> Optional[str]: pass
    
    @XWSchema(
        format="coordinates",
        description="User location"
    )
    def location(self) -> Optional[dict]: pass
```

### With Optional Types

```python
class Profile(XWEntity):
    @XWSchema(
        format="email",
        description="Optional contact email"
    )
    def contact_email(self) -> Optional[str]: pass  # Optional type = not required
    
    @XWSchema(
        format="url",
        required=True,
        description="Website URL"
    )
    def website(self) -> str: pass  # Not Optional = required (if no default)
```

## Implementation Notes

1. **Format Validation**: Each format should have appropriate validation:
   - Pattern matching for strings
   - Range validation for numbers (longitude, latitude, altitude)
   - Structure validation for objects (address, coordinates)

2. **International Standards**:
   - Address: Follow ISO 19160 or UPU S42 standards
   - Coordinates: WGS84 standard (decimal degrees)
   - Email: RFC 5322
   - Date/Time: ISO 8601

3. **Confidential Fields**: Fields like `password` should be marked as `confidential=True` in XWSchema to prevent exposure in logs or serialization.

4. **Required vs Optional**: 
   - Use `Optional[T]` type hint to indicate optional fields
   - Use `required=True` in XWSchema to explicitly mark as required
   - If not Optional and no default, field is required by default
