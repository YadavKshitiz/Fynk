package com.fynk.app.navigation

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
        composable(FynkDestinations.Permissions.route) {
            PermissionsScreen(
                onContinueClick = {
                    navController.navigate(FynkDestinations.PasswordSetup.route) {
                        popUpTo(FynkDestinations.Permissions.route) { inclusive = true }
                    }
                }
            )
        }
        composable(FynkDestinations.PasswordSetup.route) {
            PasswordSetupScreen(
                onSaveComplete = {
                    navController.navigate(FynkDestinations.Home.route) {
                        popUpTo(FynkDestinations.PasswordSetup.route) { inclusive = true }
                    }
                }
            )
        }
        composable(FynkDestinations.Home.route) { HomeScreen() }
        composable(FynkDestinations.AddApp.route) { AddAppScreen() }
        composable(FynkDestinations.SetLimit.route) { SetLimitScreen() }
        composable(FynkDestinations.Settings.route) { SettingsScreen() }
        composable(FynkDestinations.BlockScreen.route) { BlockScreenScreen() }
        composable(FynkDestinations.PasswordEntry.route) { PasswordEntryScreen() }
    }
}
