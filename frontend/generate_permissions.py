import os

base_dir = "/home/yadavkshitiz/Android/Fynk/frontend"

files = {
    "app/src/main/java/com/fynk/app/service/FynkAccessibilityService.kt": """package com.fynk.app.service

import android.accessibilityservice.AccessibilityService
import android.view.accessibility.AccessibilityEvent

class FynkAccessibilityService : AccessibilityService() {
    override fun onAccessibilityEvent(event: AccessibilityEvent?) {
        // To be implemented
    }

    override fun onInterrupt() {
        // To be implemented
    }
}
""",
    "app/src/main/java/com/fynk/app/viewmodel/PermissionsViewModel.kt": """package com.fynk.app.viewmodel

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
""",
    "app/src/main/java/com/fynk/app/ui/screens/permissions/PermissionsScreen.kt": """package com.fynk.app.ui.screens.permissions

import android.content.Intent
import android.net.Uri
import android.provider.Settings
import androidx.compose.animation.Crossfade
import androidx.compose.animation.animateColorAsState
import androidx.compose.animation.core.tween
import androidx.compose.foundation.layout.*
import androidx.compose.material.icons.Icons
import androidx.compose.material.icons.rounded.Accessibility
import androidx.compose.material.icons.rounded.BatteryChargingFull
import androidx.compose.material.icons.rounded.CheckCircle
import androidx.compose.material.icons.rounded.PictureInPicture
import androidx.compose.material3.*
import androidx.compose.runtime.*
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.platform.LocalContext
import androidx.compose.ui.platform.LocalLifecycleOwner
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.unit.dp
import androidx.lifecycle.Lifecycle
import androidx.lifecycle.LifecycleEventObserver
import androidx.lifecycle.viewmodel.compose.viewModel
import com.fynk.app.viewmodel.PermissionsViewModel
import androidx.compose.ui.draw.alpha

@Composable
fun PermissionsScreen(
    onContinueClick: () -> Unit = {},
    viewModel: PermissionsViewModel = viewModel()
) {
    val context = LocalContext.current
    val lifecycleOwner = LocalLifecycleOwner.current

    val isAccessibilityGranted by viewModel.isAccessibilityGranted.collectAsState()
    val isOverlayGranted by viewModel.isOverlayGranted.collectAsState()
    val isBatteryGranted by viewModel.isBatteryOptimizationIgnored.collectAsState()

    DisposableEffect(lifecycleOwner) {
        val observer = LifecycleEventObserver { _, event ->
            if (event == Lifecycle.Event.ON_RESUME) {
                viewModel.checkPermissions()
            }
        }
        lifecycleOwner.lifecycle.addObserver(observer)
        onDispose {
            lifecycleOwner.lifecycle.removeObserver(observer)
        }
    }

    val allGranted = isAccessibilityGranted && isOverlayGranted && isBatteryGranted

    val buttonContainerColor by animateColorAsState(
        targetValue = if (allGranted) MaterialTheme.colorScheme.primary else MaterialTheme.colorScheme.surfaceVariant,
        animationSpec = tween(durationMillis = 250),
        label = "buttonContainerColor"
    )

    val buttonContentColor by animateColorAsState(
        targetValue = if (allGranted) MaterialTheme.colorScheme.onPrimary else MaterialTheme.colorScheme.onSurfaceVariant,
        animationSpec = tween(durationMillis = 250),
        label = "buttonContentColor"
    )

    Column(
        modifier = Modifier
            .fillMaxSize()
            .padding(24.dp),
        horizontalAlignment = Alignment.CenterHorizontally
    ) {
        Spacer(modifier = Modifier.height(32.dp))
        
        Text(
            text = "One-time setup",
            style = MaterialTheme.typography.headlineMedium,
            color = MaterialTheme.colorScheme.onBackground,
            modifier = Modifier.align(Alignment.Start)
        )
        
        Spacer(modifier = Modifier.height(8.dp))
        
        Text(
            text = "Fynk needs these permissions to work properly. This only takes a minute.",
            style = MaterialTheme.typography.bodyMedium,
            color = MaterialTheme.colorScheme.onBackground.copy(alpha = 0.7f),
            modifier = Modifier.align(Alignment.Start)
        )
        
        Spacer(modifier = Modifier.height(32.dp))

        // Accessibility Card
        PermissionCard(
            title = "Accessibility",
            description = "Lets Fynk detect when a blocked app opens",
            icon = Icons.Rounded.Accessibility,
            isGranted = isAccessibilityGranted,
            onGrantClick = {
                val intent = Intent(Settings.ACTION_ACCESSIBILITY_SETTINGS)
                context.startActivity(intent)
            }
        )

        Spacer(modifier = Modifier.height(12.dp))

        // Overlay Card
        PermissionCard(
            title = "Overlay",
            description = "Allows Fynk to show the block screen",
            icon = Icons.Rounded.PictureInPicture,
            isGranted = isOverlayGranted,
            onGrantClick = {
                val intent = Intent(Settings.ACTION_MANAGE_OVERLAY_PERMISSION).apply {
                    data = Uri.parse("package:${context.packageName}")
                }
                context.startActivity(intent)
            }
        )

        Spacer(modifier = Modifier.height(12.dp))

        // Battery Card
        PermissionCard(
            title = "Battery",
            description = "Keeps Fynk running reliably in the background",
            icon = Icons.Rounded.BatteryChargingFull,
            isGranted = isBatteryGranted,
            onGrantClick = {
                try {
                    val intent = Intent(Settings.ACTION_REQUEST_IGNORE_BATTERY_OPTIMIZATIONS).apply {
                        data = Uri.parse("package:${context.packageName}")
                    }
                    context.startActivity(intent)
                } catch (e: Exception) {
                    val fallbackIntent = Intent(Settings.ACTION_IGNORE_BATTERY_OPTIMIZATION_SETTINGS)
                    context.startActivity(fallbackIntent)
                }
            }
        )

        Spacer(modifier = Modifier.weight(1f))

        Button(
            onClick = { if (allGranted) onContinueClick() },
            modifier = Modifier
                .fillMaxWidth()
                .height(56.dp)
                .alpha(if (allGranted) 1f else 0.4f),
            shape = MaterialTheme.shapes.large,
            colors = ButtonDefaults.buttonColors(
                containerColor = buttonContainerColor,
                contentColor = buttonContentColor,
                disabledContainerColor = buttonContainerColor,
                disabledContentColor = buttonContentColor
            )
        ) {
            Text(
                text = "Continue",
                style = MaterialTheme.typography.titleMedium.copy(fontWeight = FontWeight.SemiBold)
            )
        }
        
        Spacer(modifier = Modifier.height(16.dp))
    }
}

@Composable
fun PermissionCard(
    title: String,
    description: String,
    icon: androidx.compose.ui.graphics.vector.ImageVector,
    isGranted: Boolean,
    onGrantClick: () -> Unit
) {
    Card(
        modifier = Modifier.fillMaxWidth(),
        shape = MaterialTheme.shapes.large,
        colors = CardDefaults.cardColors(containerColor = MaterialTheme.colorScheme.surfaceVariant),
        elevation = CardDefaults.cardElevation(defaultElevation = 1.dp)
    ) {
        Row(
            modifier = Modifier
                .fillMaxWidth()
                .padding(16.dp),
            verticalAlignment = Alignment.CenterVertically
        ) {
            Icon(
                imageVector = icon,
                contentDescription = null,
                tint = MaterialTheme.colorScheme.primary,
                modifier = Modifier.size(24.dp)
            )

            Spacer(modifier = Modifier.width(16.dp))

            Column(modifier = Modifier.weight(1f)) {
                Text(
                    text = title,
                    style = MaterialTheme.typography.titleMedium,
                    color = MaterialTheme.colorScheme.onSurfaceVariant
                )
                Text(
                    text = description,
                    style = MaterialTheme.typography.bodySmall,
                    color = MaterialTheme.colorScheme.onSurfaceVariant.copy(alpha = 0.7f)
                )
            }

            Spacer(modifier = Modifier.width(16.dp))

            Crossfade(
                targetState = isGranted,
                animationSpec = tween(durationMillis = 200),
                label = "permission_status"
            ) { granted ->
                if (granted) {
                    Icon(
                        imageVector = Icons.Rounded.CheckCircle,
                        contentDescription = "Granted",
                        tint = Color(0xFF4CAF50), // Success green
                        modifier = Modifier.size(24.dp)
                    )
                } else {
                    OutlinedButton(onClick = onGrantClick) {
                        Text("Grant")
                    }
                }
            }
        }
    }
}
"""
}

for path, content in files.items():
    full_path = os.path.join(base_dir, path)
    os.makedirs(os.path.dirname(full_path), exist_ok=True)
    with open(full_path, "w") as f:
        f.write(content)

print("Files created.")
