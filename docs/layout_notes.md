# TRENCH Faceplate Layout Notes

## Canonical Asset
- Source faceplate render is @3x.
- Master asset: 1800 x 2702 px.
- Recommended corrected asset: 1800 x 2703 px for clean 600 x 901 @1x UI.

## Measured @3x

| Element | Width | Height |
|--------|-------|-------|
| Main display | 1350 px | 715 px |
| Top slot | 1215 px | 102 px |
| Morph/Q wells | 920 px | 146 px |
| Value boxes | 296 px | 121 px |

## Implied @1x

| Element | Width | Height |
|--------|-------|-------|
| Main display | 450.0f | 238.333f |
| Top slot | 405.0f | 34.0f |
| Morph/Q wells | 306.667f | 48.667f |
| Value boxes | 98.667f | 40.333f |

## Implementation Rule

Use the 3x asset coordinates as canonical, then divide by 3.0f in layout helpers. Do not manually round each measurement.

```cpp
static constexpr float assetScale = 3.0f;

static juce::Rectangle<float> from3x(float x, float y, float w, float h)
{
    return {
        x / assetScale,
        y / assetScale,
        w / assetScale,
        h / assetScale
    };
}
```

Then only snap at the final component boundary:

```cpp
component.setBounds(from3x(x, y, w, h).getSmallestIntegerContainer());
```

For drawing graph/bar geometry, keep floats. That avoids the 1px shimmy.