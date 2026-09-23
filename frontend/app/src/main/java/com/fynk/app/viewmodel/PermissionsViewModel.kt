package com.fynk.app.viewmodel

import android.app.Application
import android.content.Context
import android.os.PowerManager
import android.provider.Settings
import androidx.lifecycle.AndroidViewModel
import kotlinx.coroutines.flow.MutableStateFlow
import kotlinx.coroutines.flow.StateFlow
import kotlinx.coroutines.flow.asStateFlow

class PermissionsViewModel(application: Application) : AndroidViewModel(application) {

    private val _isAccessibilityGranted = MutableStateFlow(false)
    val isAccessibilityGranted: StateFlow<Boolean> = _isAccessibilityGranted.asStateFlow()

    private val _isOverlayGranted = MutableStateFlow(false)
    val isOverlayGranted: StateFlow<Boolean> = _isOverlayGranted.asStateFlow()

    private val _isBatteryOptimizationIgnored = MutableStateFlow(false)
    val isBatteryOptimizationIgnored: StateFlow<Boolean> = _isBatteryOptimizationIgnored.asStateFlow()

    fun checkPermissions() {
        val context = getApplication<Application>()
        
        // 1. Check Accessibility
        val accessibilityEnabled = Settings.Secure.getInt(
            context.contentResolver,
            Settings.Secure.ACCESSIBILITY_ENABLED, 0
        )
        var isAccessibilityGranted = false
        if (accessibilityEnabled == 1) {
            val enabledServices = Settings.Secure.getString(
                context.contentResolver,
                Settings.Secure.ENABLED_ACCESSIBILITY_SERVICES
            )
            val expectedComponentName = "${context.packageName}/com.fynk.app.service.FynkAccessibilityService"
            isAccessibilityGranted = enabledServices?.contains(expectedComponentName) == true
        }
        _isAccessibilityGranted.value = isAccessibilityGranted

        // 2. Check Overlay
        _isOverlayGranted.value = Settings.canDrawOverlays(context)

        // 3. Check Battery Optimization
        val powerManager = context.getSystemService(Context.POWER_SERVICE) as PowerManager
        _isBatteryOptimizationIgnored.value = powerManager.isIgnoringBatteryOptimizations(context.packageName)
    }
}
