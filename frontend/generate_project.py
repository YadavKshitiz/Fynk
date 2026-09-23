import os

base_dir = "/home/yadavkshitiz/Android/Fynk/frontend"

files = {
    "gradle/libs.versions.toml": """[versions]
agp = "8.4.2"
kotlin = "2.0.0"
coreKtx = "1.13.1"
lifecycleRuntimeKtx = "2.8.2"
activityCompose = "1.9.0"
composeBom = "2024.06.00"
room = "2.6.1"
datastore = "1.1.1"
ktor = "2.3.11"
serialization = "1.6.3"
coil = "2.6.0"
ksp = "2.0.0-1.0.21"
navigationCompose = "2.7.7"

[libraries]
androidx-core-ktx = { group = "androidx.core", name = "core-ktx", version.ref = "coreKtx" }
androidx-lifecycle-runtime-ktx = { group = "androidx.lifecycle", name = "lifecycle-runtime-ktx", version.ref = "lifecycleRuntimeKtx" }
androidx-lifecycle-viewmodel-compose = { group = "androidx.lifecycle", name = "lifecycle-viewmodel-compose", version.ref = "lifecycleRuntimeKtx" }
androidx-activity-compose = { group = "androidx.activity", name = "activity-compose", version.ref = "activityCompose" }
androidx-compose-bom = { group = "androidx.compose", name = "compose-bom", version.ref = "composeBom" }
androidx-ui = { group = "androidx.compose.ui", name = "ui" }
androidx-ui-graphics = { group = "androidx.compose.ui", name = "ui-graphics" }
androidx-ui-tooling = { group = "androidx.compose.ui", name = "ui-tooling" }
androidx-ui-tooling-preview = { group = "androidx.compose.ui", name = "ui-tooling-preview" }
androidx-material3 = { group = "androidx.compose.material3", name = "material3" }
androidx-navigation-compose = { group = "androidx.navigation", name = "navigation-compose", version.ref = "navigationCompose" }

room-runtime = { group = "androidx.room", name = "room-runtime", version.ref = "room" }
room-ktx = { group = "androidx.room", name = "room-ktx", version.ref = "room" }
room-compiler = { group = "androidx.room", name = "room-compiler", version.ref = "room" }

datastore-preferences = { group = "androidx.datastore", name = "datastore-preferences", version.ref = "datastore" }

ktor-client-core = { group = "io.ktor", name = "ktor-client-core", version.ref = "ktor" }
ktor-client-android = { group = "io.ktor", name = "ktor-client-android", version.ref = "ktor" }
ktor-client-content-negotiation = { group = "io.ktor", name = "ktor-client-content-negotiation", version.ref = "ktor" }
ktor-serialization-kotlinx-json = { group = "io.ktor", name = "ktor-serialization-kotlinx-json", version.ref = "ktor" }

kotlinx-serialization-json = { group = "org.jetbrains.kotlinx", name = "kotlinx-serialization-json", version.ref = "serialization" }

coil-compose = { group = "io.coil-kt", name = "coil-compose", version.ref = "coil" }

[plugins]
android-application = { id = "com.android.application", version.ref = "agp" }
kotlin-android = { id = "org.jetbrains.kotlin.android", version.ref = "kotlin" }
kotlin-plugin-compose = { id = "org.jetbrains.kotlin.plugin.compose", version.ref = "kotlin" }
kotlin-serialization = { id = "org.jetbrains.kotlin.plugin.serialization", version.ref = "kotlin" }
ksp = { id = "com.google.devtools.ksp", version.ref = "ksp" }
""",
    "settings.gradle.kts": """pluginManagement {
    repositories {
        google {
            content {
                includeGroupByRegex("com\\\\.android.*")
                includeGroupByRegex("com\\\\.google.*")
                includeGroupByRegex("androidx.*")
            }
        }
        mavenCentral()
        gradlePluginPortal()
    }
}
dependencyResolutionManagement {
    repositoriesMode.set(RepositoriesMode.FAIL_ON_PROJECT_REPOS)
    repositories {
        google()
        mavenCentral()
    }
}

rootProject.name = "Fynk"
include(":app")
""",
    "build.gradle.kts": """plugins {
    alias(libs.plugins.android.application) apply false
    alias(libs.plugins.kotlin.android) apply false
    alias(libs.plugins.kotlin.plugin.compose) apply false
    alias(libs.plugins.kotlin.serialization) apply false
    alias(libs.plugins.ksp) apply false
}
""",
    "gradle.properties": """org.gradle.jvmargs=-Xmx2048m -Dfile.encoding=UTF-8
android.useAndroidX=true
kotlin.code.style=official
""",
    "app/build.gradle.kts": """plugins {
    alias(libs.plugins.android.application)
    alias(libs.plugins.kotlin.android)
    alias(libs.plugins.kotlin.plugin.compose)
    alias(libs.plugins.kotlin.serialization)
    alias(libs.plugins.ksp)
}

android {
    namespace = "com.fynk.app"
    compileSdk = 35

    defaultConfig {
        applicationId = "com.fynk.app"
        minSdk = 26
        targetSdk = 35
        versionCode = 1
        versionName = "1.0"

        testInstrumentationRunner = "androidx.test.runner.AndroidJUnitRunner"
        vectorDrawables {
            useSupportLibrary = true
        }
    }

    buildTypes {
        release {
            isMinifyEnabled = false
            proguardFiles(
                getDefaultProguardFile("proguard-android-optimize.txt"),
                "proguard-rules.pro"
            )
        }
    }
    compileOptions {
        sourceCompatibility = JavaVersion.VERSION_17
        targetCompatibility = JavaVersion.VERSION_17
    }
    kotlinOptions {
        jvmTarget = "17"
    }
    buildFeatures {
        compose = true
    }
    packaging {
        resources {
            excludes += "/META-INF/{AL2.0,LGPL2.1}"
        }
    }
}

dependencies {
    implementation(libs.androidx.core.ktx)
    implementation(libs.androidx.lifecycle.runtime.ktx)
    implementation(libs.androidx.lifecycle.viewmodel.compose)
    implementation(libs.androidx.activity.compose)
    implementation(platform(libs.androidx.compose.bom))
    implementation(libs.androidx.ui)
    implementation(libs.androidx.ui.graphics)
    implementation(libs.androidx.ui.tooling.preview)
    implementation(libs.androidx.material3)
    implementation(libs.androidx.navigation.compose)

    implementation(libs.room.runtime)
    implementation(libs.room.ktx)
    ksp(libs.room.compiler)

    implementation(libs.datastore.preferences)

    implementation(libs.ktor.client.core)
    implementation(libs.ktor.client.android)
    implementation(libs.ktor.client.content.negotiation)
    implementation(libs.ktor.serialization.kotlinx.json)
    implementation(libs.kotlinx.serialization.json)

    implementation(libs.coil.compose)

    debugImplementation(libs.androidx.ui.tooling)
}
""",
    "app/src/main/AndroidManifest.xml": """<?xml version="1.0" encoding="utf-8"?>
<manifest xmlns:android="http://schemas.android.com/apk/res/android"
    xmlns:tools="http://schemas.android.com/tools">

    <application
        android:allowBackup="true"
        android:dataExtractionRules="@xml/data_extraction_rules"
        android:fullBackupContent="@xml/backup_rules"
        android:icon="@mipmap/ic_launcher"
        android:label="@string/app_name"
        android:roundIcon="@mipmap/ic_launcher_round"
        android:supportsRtl="true"
        android:theme="@style/Theme.Fynk"
        tools:targetApi="35">
        <activity
            android:name=".MainActivity"
            android:exported="true"
            android:theme="@style/Theme.Fynk">
            <intent-filter>
                <action android:name="android.intent.action.MAIN" />
                <category android:name="android.intent.category.LAUNCHER" />
            </intent-filter>
        </activity>
    </application>

</manifest>
""",
    "app/src/main/res/xml/backup_rules.xml": """<?xml version="1.0" encoding="utf-8"?>
<full-backup-content xmlns:android="http://schemas.android.com/apk/res/android">
    <include domain="sharedpref" path="."/>
    <exclude domain="sharedpref" path="device.xml"/>
</full-backup-content>
""",
    "app/src/main/res/xml/data_extraction_rules.xml": """<?xml version="1.0" encoding="utf-8"?>
<data-extraction-rules>
    <cloud-backup>
        <include domain="sharedpref" path="."/>
        <exclude domain="sharedpref" path="device.xml"/>
    </cloud-backup>
    <device-transfer>
        <include domain="sharedpref" path="."/>
        <exclude domain="sharedpref" path="device.xml"/>
    </device-transfer>
</data-extraction-rules>
""",
    "app/src/main/res/values/strings.xml": """<resources>
    <string name="app_name">Fynk</string>
</resources>
""",
    "app/src/main/res/values/themes.xml": """<?xml version="1.0" encoding="utf-8"?>
<resources>
    <style name="Theme.Fynk" parent="android:Theme.Material.Light.NoActionBar" />
</resources>
""",
    "app/src/main/res/drawable/ic_launcher_background.xml": """<?xml version="1.0" encoding="utf-8"?>
<vector xmlns:android="http://schemas.android.com/apk/res/android"
    android:width="108dp"
    android:height="108dp"
    android:viewportWidth="108"
    android:viewportHeight="108">
    <path
        android:fillColor="#4FC3F7"
        android:pathData="M0,0h108v108h-108z" />
</vector>
""",
    "app/src/main/res/drawable/ic_launcher_foreground.xml": """<?xml version="1.0" encoding="utf-8"?>
<vector xmlns:android="http://schemas.android.com/apk/res/android"
    android:width="108dp"
    android:height="108dp"
    android:viewportWidth="108"
    android:viewportHeight="108">
    <!-- A simple "F" in white -->
    <path
        android:fillColor="#FFFFFF"
        android:pathData="M 38 28 L 74 28 L 74 40 L 52 40 L 52 52 L 68 52 L 68 64 L 52 64 L 52 84 L 38 84 Z" />
</vector>
""",
    "app/src/main/res/mipmap-anydpi-v26/ic_launcher.xml": """<?xml version="1.0" encoding="utf-8"?>
<adaptive-icon xmlns:android="http://schemas.android.com/apk/res/android">
    <background android:drawable="@drawable/ic_launcher_background" />
    <foreground android:drawable="@drawable/ic_launcher_foreground" />
</adaptive-icon>
""",
    "app/src/main/res/mipmap-anydpi-v26/ic_launcher_round.xml": """<?xml version="1.0" encoding="utf-8"?>
<adaptive-icon xmlns:android="http://schemas.android.com/apk/res/android">
    <background android:drawable="@drawable/ic_launcher_background" />
    <foreground android:drawable="@drawable/ic_launcher_foreground" />
</adaptive-icon>
""",
    "app/src/main/java/com/fynk/app/MainActivity.kt": """package com.fynk.app

import android.os.Bundle
import androidx.activity.ComponentActivity
import androidx.activity.compose.setContent
import androidx.activity.enableEdgeToEdge
import androidx.compose.foundation.layout.fillMaxSize
import androidx.compose.foundation.layout.padding
import androidx.compose.material3.Scaffold
import androidx.compose.ui.Modifier
import com.fynk.app.ui.theme.FynkTheme
import com.fynk.app.navigation.FynkNavHost

class MainActivity : ComponentActivity() {
    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        enableEdgeToEdge()
        setContent {
            FynkTheme {
                Scaffold(modifier = Modifier.fillMaxSize()) { innerPadding ->
                    FynkNavHost(modifier = Modifier.padding(innerPadding))
                }
            }
        }
    }
}
""",
    "app/src/main/java/com/fynk/app/ui/theme/Theme.kt": """package com.fynk.app.ui.theme

import androidx.compose.foundation.isSystemInDarkTheme
import androidx.compose.material3.MaterialTheme
import androidx.compose.material3.darkColorScheme
import androidx.compose.material3.lightColorScheme
import androidx.compose.runtime.Composable

private val DarkColorScheme = darkColorScheme(
    primary = Purple80,
    secondary = PurpleGrey80,
    tertiary = Pink80
)

private val LightColorScheme = lightColorScheme(
    primary = Purple40,
    secondary = PurpleGrey40,
    tertiary = Pink40
)

@Composable
fun FynkTheme(
    darkTheme: Boolean = isSystemInDarkTheme(),
    content: @Composable () -> Unit
) {
    val colorScheme = if (darkTheme) {
        DarkColorScheme
    } else {
        LightColorScheme
    }

    MaterialTheme(
        colorScheme = colorScheme,
        typography = Typography,
        content = content
    )
}
""",
    "app/src/main/java/com/fynk/app/ui/theme/Color.kt": """package com.fynk.app.ui.theme

import androidx.compose.ui.graphics.Color

val Purple80 = Color(0xFFD0BCFF)
val PurpleGrey80 = Color(0xFFCCC2DC)
val Pink80 = Color(0xFFEFB8C8)

val Purple40 = Color(0xFF6650a4)
val PurpleGrey40 = Color(0xFF625b71)
val Pink40 = Color(0xFF7D5260)
""",
    "app/src/main/java/com/fynk/app/ui/theme/Type.kt": """package com.fynk.app.ui.theme

import androidx.compose.material3.Typography
import androidx.compose.ui.text.TextStyle
import androidx.compose.ui.text.font.FontFamily
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.unit.sp

val Typography = Typography(
    bodyLarge = TextStyle(
        fontFamily = FontFamily.Default,
        fontWeight = FontWeight.Normal,
        fontSize = 16.sp,
        lineHeight = 24.sp,
        letterSpacing = 0.5.sp
    )
)
""",
    "app/src/main/java/com/fynk/app/navigation/FynkDestinations.kt": """package com.fynk.app.navigation

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
import com.fynk.app.ui.screens.blockscreen.BlockScreen
import com.fynk.app.ui.screens.passwordentry.PasswordEntryScreen

@Composable
fun FynkNavHost(modifier: Modifier = Modifier) {
    val navController = rememberNavController()

    NavHost(
        navController = navController,
        startDestination = FynkDestinations.Onboarding.route,
        modifier = modifier
    ) {
        composable(FynkDestinations.Onboarding.route) { OnboardingScreen() }
        composable(FynkDestinations.Permissions.route) { PermissionsScreen() }
        composable(FynkDestinations.PasswordSetup.route) { PasswordSetupScreen() }
        composable(FynkDestinations.Home.route) { HomeScreen() }
        composable(FynkDestinations.AddApp.route) { AddAppScreen() }
        composable(FynkDestinations.SetLimit.route) { SetLimitScreen() }
        composable(FynkDestinations.Settings.route) { SettingsScreen() }
        composable(FynkDestinations.BlockScreen.route) { BlockScreen() }
        composable(FynkDestinations.PasswordEntry.route) { PasswordEntryScreen() }
    }
}
""",
}

# Create placeholder screens
screens = ["onboarding", "permissions", "passwordsetup", "home", "addapp", "setlimit", "settings", "blockscreen", "passwordentry"]

for screen in screens:
    class_name = "".join(word.capitalize() for word in screen.split("_"))
    if screen == "onboarding": class_name = "Onboarding"
    elif screen == "permissions": class_name = "Permissions"
    elif screen == "passwordsetup": class_name = "PasswordSetup"
    elif screen == "home": class_name = "Home"
    elif screen == "addapp": class_name = "AddApp"
    elif screen == "setlimit": class_name = "SetLimit"
    elif screen == "settings": class_name = "Settings"
    elif screen == "blockscreen": class_name = "BlockScreen"
    elif screen == "passwordentry": class_name = "PasswordEntry"
    
    file_path = f"app/src/main/java/com/fynk/app/ui/screens/{screen}/{class_name}Screen.kt"
    content = f"""package com.fynk.app.ui.screens.{screen}

import androidx.compose.foundation.layout.Box
import androidx.compose.foundation.layout.fillMaxSize
import androidx.compose.material3.Text
import androidx.compose.runtime.Composable
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier

@Composable
fun {class_name}Screen() {{
    Box(modifier = Modifier.fillMaxSize(), contentAlignment = Alignment.Center) {{
        Text("{class_name} Screen")
    }}
}}
"""
    files[file_path] = content

for path, content in files.items():
    full_path = os.path.join(base_dir, path)
    os.makedirs(os.path.dirname(full_path), exist_ok=True)
    with open(full_path, "w") as f:
        f.write(content)

print("Files created.")
