import os

base_dir = "/home/yadavkshitiz/Android/Fynk/frontend"

files = {
    "app/src/main/java/com/fynk/app/data/datastore/OnboardingPreferenceRepository.kt": """package com.fynk.app.data.datastore

import android.content.Context
import androidx.datastore.preferences.core.booleanPreferencesKey
import androidx.datastore.preferences.core.edit
import kotlinx.coroutines.flow.Flow
import kotlinx.coroutines.flow.map

class OnboardingPreferenceRepository(private val context: Context) {
    private val HAS_SEEN_ONBOARDING_KEY = booleanPreferencesKey("has_seen_onboarding")

    val hasSeenOnboardingFlow: Flow<Boolean> = context.dataStore.data.map { preferences ->
        preferences[HAS_SEEN_ONBOARDING_KEY] ?: false
    }

    suspend fun setHasSeenOnboarding(hasSeen: Boolean) {
        context.dataStore.edit { preferences ->
            preferences[HAS_SEEN_ONBOARDING_KEY] = hasSeen
        }
    }
}
""",
    "app/src/main/java/com/fynk/app/ui/screens/onboarding/OnboardingScreen.kt": """package com.fynk.app.ui.screens.onboarding

import androidx.compose.animation.core.Animatable
import androidx.compose.animation.core.tween
import androidx.compose.foundation.background
import androidx.compose.foundation.layout.*
import androidx.compose.material.icons.Icons
import androidx.compose.material.icons.rounded.Shield
import androidx.compose.material3.Button
import androidx.compose.material3.Icon
import androidx.compose.material3.MaterialTheme
import androidx.compose.material3.Text
import androidx.compose.runtime.Composable
import androidx.compose.runtime.LaunchedEffect
import androidx.compose.runtime.remember
import androidx.compose.runtime.rememberCoroutineScope
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.draw.alpha
import androidx.compose.ui.graphics.graphicsLayer
import androidx.compose.ui.platform.LocalContext
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.text.style.TextAlign
import androidx.compose.ui.unit.dp
import androidx.navigation.NavController
import com.fynk.app.data.datastore.OnboardingPreferenceRepository
import com.fynk.app.navigation.FynkDestinations
import kotlinx.coroutines.launch

@Composable
fun OnboardingScreen(navController: NavController) {
    val context = LocalContext.current
    val coroutineScope = rememberCoroutineScope()
    val onboardingRepository = remember { OnboardingPreferenceRepository(context) }

    val iconScale = remember { Animatable(0.8f) }
    val iconAlpha = remember { Animatable(0f) }
    
    val contentOffset = remember { Animatable(40f) }
    val contentAlpha = remember { Animatable(0f) }

    LaunchedEffect(Unit) {
        launch {
            iconAlpha.animateTo(1f, animationSpec = tween(500))
        }
        launch {
            iconScale.animateTo(1f, animationSpec = tween(500))
        }
        
        // Delay content animation
        kotlinx.coroutines.delay(200)
        
        launch {
            contentAlpha.animateTo(1f, animationSpec = tween(400))
        }
        launch {
            contentOffset.animateTo(0f, animationSpec = tween(400))
        }
    }

    Box(
        modifier = Modifier
            .fillMaxSize()
            .background(MaterialTheme.colorScheme.background)
            .padding(horizontal = 24.dp),
        contentAlignment = Alignment.Center
    ) {
        Column(
            horizontalAlignment = Alignment.CenterHorizontally,
            verticalArrangement = Arrangement.Center,
            modifier = Modifier.fillMaxWidth()
        ) {
            Icon(
                imageVector = Icons.Rounded.Shield,
                contentDescription = null,
                tint = MaterialTheme.colorScheme.primary,
                modifier = Modifier
                    .size(96.dp)
                    .graphicsLayer {
                        scaleX = iconScale.value
                        scaleY = iconScale.value
                        alpha = iconAlpha.value
                    }
            )
            
            Spacer(modifier = Modifier.height(32.dp))
            
            Column(
                horizontalAlignment = Alignment.CenterHorizontally,
                modifier = Modifier.graphicsLayer {
                    translationY = contentOffset.value.dp.toPx()
                    alpha = contentAlpha.value
                }
            ) {
                Text(
                    text = "Take back your focus",
                    style = MaterialTheme.typography.headlineMedium,
                    color = MaterialTheme.colorScheme.onBackground
                )
                
                Spacer(modifier = Modifier.height(16.dp))
                
                Text(
                    text = "Fynk helps you set real limits on distracting apps — and gives a trusted friend the final say when you want to break them.",
                    style = MaterialTheme.typography.bodyLarge,
                    color = MaterialTheme.colorScheme.onBackground.copy(alpha = 0.7f),
                    textAlign = TextAlign.Center
                )
                
                Spacer(modifier = Modifier.height(48.dp))
                
                Button(
                    onClick = {
                        coroutineScope.launch {
                            onboardingRepository.setHasSeenOnboarding(true)
                            navController.navigate(FynkDestinations.Permissions.route) {
                                popUpTo(FynkDestinations.Onboarding.route) { inclusive = true }
                            }
                        }
                    },
                    modifier = Modifier
                        .fillMaxWidth()
                        .height(56.dp),
                    shape = MaterialTheme.shapes.large
                ) {
                    Text(
                        text = "Get Started",
                        style = MaterialTheme.typography.titleMedium.copy(fontWeight = FontWeight.SemiBold)
                    )
                }
            }
        }
    }
}
""",
    "app/src/main/java/com/fynk/app/navigation/FynkNavHost.kt": """package com.fynk.app.navigation

import androidx.compose.runtime.Composable
import androidx.compose.ui.Modifier
import androidx.navigation.compose.NavHost
import androidx.navigation.compose.composable
import androidx.navigation.compose.rememberNavController
import com.fynk.app.ui.screens.onboarding.OnboardingScreen
import com.fynk.app.ui.screens.permissions.PermissionsScreen
import com.fynk.app.ui.screens.passwordsetup.PasswordSetupScreen
import com.fynk.app.ui.screens.home.HomeScreen
import com.fynk.app.ui.screens.addapp.AddAppScreen
import com.fynk.app.ui.screens.setlimit.SetLimitScreen
import com.fynk.app.ui.screens.settings.SettingsScreen
import com.fynk.app.ui.screens.blockscreen.BlockScreenScreen
import com.fynk.app.ui.screens.passwordentry.PasswordEntryScreen

@Composable
fun FynkNavHost(
    startDestination: String = FynkDestinations.Onboarding.route,
    modifier: Modifier = Modifier
) {
    val navController = rememberNavController()

    NavHost(
        navController = navController,
        startDestination = startDestination,
        modifier = modifier
    ) {
        composable(FynkDestinations.Onboarding.route) { OnboardingScreen(navController) }
        composable(FynkDestinations.Permissions.route) { PermissionsScreen() }
        composable(FynkDestinations.PasswordSetup.route) { PasswordSetupScreen() }
        composable(FynkDestinations.Home.route) { HomeScreen() }
        composable(FynkDestinations.AddApp.route) { AddAppScreen() }
        composable(FynkDestinations.SetLimit.route) { SetLimitScreen() }
        composable(FynkDestinations.Settings.route) { SettingsScreen() }
        composable(FynkDestinations.BlockScreen.route) { BlockScreenScreen() }
        composable(FynkDestinations.PasswordEntry.route) { PasswordEntryScreen() }
    }
}
""",
    "app/src/main/java/com/fynk/app/MainActivity.kt": """package com.fynk.app

import android.os.Bundle
import androidx.activity.ComponentActivity
import androidx.activity.compose.setContent
import androidx.activity.enableEdgeToEdge
import androidx.compose.foundation.layout.fillMaxSize
import androidx.compose.foundation.layout.padding
import androidx.compose.material3.Scaffold
import androidx.compose.runtime.collectAsState
import androidx.compose.runtime.getValue
import androidx.compose.ui.Modifier
import com.fynk.app.data.datastore.AppTheme
import com.fynk.app.data.datastore.OnboardingPreferenceRepository
import com.fynk.app.data.datastore.ThemePreferenceRepository
import com.fynk.app.ui.theme.FynkTheme
import com.fynk.app.navigation.FynkNavHost
import com.fynk.app.navigation.FynkDestinations

class MainActivity : ComponentActivity() {
    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        enableEdgeToEdge()
        val themeRepository = ThemePreferenceRepository(this)
        val onboardingRepository = OnboardingPreferenceRepository(this)
        
        setContent {
            val theme by themeRepository.themeFlow.collectAsState(initial = AppTheme.SKY)
            val hasSeenOnboarding by onboardingRepository.hasSeenOnboardingFlow.collectAsState(initial = null)
            
            FynkTheme(theme = theme) {
                Scaffold(modifier = Modifier.fillMaxSize()) { innerPadding ->
                    if (hasSeenOnboarding != null) {
                        val startDestination = if (hasSeenOnboarding == true) {
                            FynkDestinations.Permissions.route
                        } else {
                            FynkDestinations.Onboarding.route
                        }
                        FynkNavHost(
                            startDestination = startDestination,
                            modifier = Modifier.padding(innerPadding)
                        )
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
