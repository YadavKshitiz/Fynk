package com.fynk.app

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
