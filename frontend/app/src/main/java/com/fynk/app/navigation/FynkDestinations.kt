package com.fynk.app.navigation

sealed class FynkDestinations(val route: String) {
    object Onboarding : FynkDestinations("onboarding")
    object Permissions : FynkDestinations("permissions")
    object PasswordSetup : FynkDestinations("passwordsetup")
    object Home : FynkDestinations("home")
    object AddApp : FynkDestinations("addapp")
    object SetLimit : FynkDestinations("setlimit")
    object Settings : FynkDestinations("settings")
    object BlockScreen : FynkDestinations("blockscreen")
    object PasswordEntry : FynkDestinations("passwordentry")
}
