#include <iostream>
#include <string>
#include <vector>
#include <memory>

// Base class for all smart devices
class SmartDevice {
public:
    virtual void turnOn() = 0;
    virtual void turnOff() = 0;
    virtual std::string getStatus() = 0;
    virtual ~SmartDevice() {}
};

// Smart thermostat class
class SmartThermostat : public SmartDevice {
private:
    std::string name;
    float currentTemperature;
    float targetTemperature;

public:
    SmartThermostat(std::string deviceName) 
        : name(deviceName), currentTemperature(22.0), targetTemperature(22.0) {}

    void setTargetTemperature(float temp) {
        targetTemperature = temp;
    }

    void turnOn() override {
        std::cout << name << " is now heating to " << targetTemperature << "°C." << std::endl;
    }

    void turnOff() override {
        std::cout << name << " is turned off." << std::endl;
    }

    std::string getStatus() override {
        return name + " is currently set to " + std::to_string(targetTemperature) + "°C.";
    }
};

// Smart light class
class SmartLight : public SmartDevice {
private:
    std::string name;
    bool isOn;
    int brightness;

public:
    SmartLight(std::string deviceName) 
        : name(deviceName), isOn(false), brightness(0) {}

    void setBrightness(int level) {
        brightness = level;
        isOn = (brightness > 0);
    }

    void turnOn() override {
        isOn = true;
        std::cout << name << " is turned on with brightness level " << brightness << "." << std::endl;
    }

    void turnOff() override {
        isOn = false;
        std::cout << name << " is turned off." << std::endl;
    }

    std::string getStatus() override {
        return name + (isOn ? " is on." : " is off.") + " Brightness level: " + std::to_string(brightness);
    }
};

// Smart home class to manage devices
class SmartHome {
private:
    std::vector<std::unique_ptr<SmartDevice>> devices;

public:
    void addDevice(std::unique_ptr<SmartDevice> device) {
        devices.push_back(std::move(device));
    }

    void controlDevices() {
        for (const auto& device : devices) {
            std::cout << device->getStatus() << std::endl;
            device->turnOn();
        }
    }

    void turnOffAll() {
        for (const auto& device : devices) {
            device->turnOff();
        }
    }
};

int main() {
    SmartHome mySmartHome;

    // Adding devices
    mySmartHome.addDevice(std::make_unique<SmartThermostat>("Living Room Thermostat"));
    mySmartHome.addDevice(std::make_unique<SmartLight>("Living Room Light"));

    // Set up devices
    static_cast<SmartThermostat*>(mySmartHome.devices[0].get())->setTargetTemperature(21.5);
    static_cast<SmartLight*>(mySmartHome.devices[1].get())->setBrightness(75);

    // Control devices
    mySmartHome.controlDevices();

    // Turn off all devices
    mySmartHome.turnOffAll();

    return 0;
}
