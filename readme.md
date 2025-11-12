# ESPHome-Devices

This repository gathers several **[ESPHome](https://esphome.io/)** configurations developed for DIY IoT devices.  
Each project is standalone but shares a common base configuration to simplify maintenance and updates.

---

## Device Summary

| Device Name | File(s) | Platform | Description | Main Features |
|--------------|----------|-----------|--------------|----------------|
| **Bedside Lamp** | `esp-lampe-chevet.yaml` | ESP8266 | Smart bedside lamp integrated with Home Assistant | Adjustable RGB light, brightness control, sunrise wake-up effect |
| **Hallway Lamp** | `esp-lampe-couloir.yaml` | ESP8266 | Automatic hallway light | Motion or schedule-based control, HA integration |
| **Dual Smart Plug** | `esp-plug-2x.yaml` | ESP8266 | Dual controllable smart plug | Two independent outlets, optional power monitoring |
| **Smart Mood Lights (x3)** | `smart-mood-light.yaml`, `smart-mood-light-ii.yaml`, `smart-mood-light-iii.yaml` | **BK7231N (LSC Smart Connect)** | Commercial LSC Smart Connect lamps reflashed with ESPHome | RGB control, local-only operation, shared config (`common-smart-mood-light.yaml`) |

---

## Repository Structure
ESPHome-Devices/  
├── common.yaml  
├── common-smart-mood-light.yaml  
├── esp-lampe-chevet.yaml  
├── esp-lampe-couloir.yaml  
├── esp-plug-2x.yaml  
├── smart-mood-light.yaml  
├── smart-mood-light-ii.yaml  
├── smart-mood-light-iii.yaml  
└── .gitignore  
  
---

## Projects

### Bedside Lamp (`esp-lampe-chevet.yaml`)
A connected **bedside lamp** powered by ESPHome and integrated with Home Assistant.  
Main features:
- Adjustable brightness and RGB color control  
- Full Home Assistant integration via the ESPHome API  
- **Sunrise effect** : the lamp gradually brightens in the morning to simulate natural light and help you wake up gently.

### Hallway Lamp (`esp-lampe-couloir.yaml`)
A connected RGB hallway light, ideal for automatic or nighttime lighting.  
Features:
- Home Assistant control

### Dual Smart Plug (`esp-plug-2x.yaml`)
A **dual smart plug** with two individually controlled outlets.  
Features:
- Independent on/off control for each outlet
- Full Home Assistant automation integration

### Smart Mood Lights  
Files:  
- `smart-mood-light.yaml`  
- `smart-mood-light-ii.yaml`  
- `smart-mood-light-iii.yaml`

These three devices are **identical commercial LSC Smart Connect lamps** that have been **flashed with custom ESPHome firmware**, replacing the original Tuya firmware.  
This conversion makes them **fully local, privacy-friendly smart lights** controllable via Home Assistant or ESPHome.  

Each lamp configuration is nearly identical, except for unique names, API keys, or entity IDs.

Shared configuration and substitutions are defined in `common-smart-mood-light.yaml`.
 
Features:
- Custom lighting effects  
- Shared configuration via `common-smart-mood-light.yaml`

### Common Files
- **`common.yaml`**: shared parameters (Wi-Fi, API, OTA, etc.)
- **`common-smart-mood-light.yaml`**: common configuration for mood light devices to avoid code duplication.

---

## License

This project is licensed under the [MIT License](LICENSE).
