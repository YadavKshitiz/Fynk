import os

base_dir = "/home/yadavkshitiz/Android/Fynk/frontend/app/src/main/java/com/fynk/app"

files = {
    "ui/theme/Color.kt": """package com.fynk.app.ui.theme

import androidx.compose.ui.graphics.Color

val SkyPrimary = Color(0xFF4FC3F7)
val SkyPrimaryContainer = Color(0xFFE1F5FE)
val SkySecondary = Color(0xFF81D4FA)
val SkyBackground = Color(0xFFFFFFFF)
val SkySurface = Color(0xFFF5FBFF)
val SkyOnPrimary = Color(0xFFFFFFFF)
val SkyOnBackground = Color(0xFF1A1A1A)
val SkyError = Color(0xFFB3261E)

val SlatePrimary = Color(0xFF90A4AE)
val SlatePrimaryContainer = Color(0xFF263238)
val SlateSecondary = Color(0xFF78909C)
val SlateBackground = Color(0xFF121212)
val SlateSurface = Color(0xFF1E1E1E)
val SlateOnPrimary = Color(0xFF000000)
val SlateOnBackground = Color(0xFFECECEC)
val SlateError = Color(0xFFCF6679)
""",
    "ui/theme/Shape.kt": """package com.fynk.app.ui.theme

import androidx.compose.foundation.shape.RoundedCornerShape
import androidx.compose.material3.Shapes
import androidx.compose.ui.unit.dp

val Shapes = Shapes(
    small = RoundedCornerShape(8.dp),
    medium = RoundedCornerShape(16.dp),
    large = RoundedCornerShape(24.dp),
    extraLarge = RoundedCornerShape(32.dp)
)
""",
    "ui/theme/Type.kt": """package com.fynk.app.ui.theme

import androidx.compose.material3.Typography
import androidx.compose.ui.text.TextStyle
import androidx.compose.ui.text.font.FontFamily
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.text.googlefonts.Font
import androidx.compose.ui.text.googlefonts.GoogleFont
import androidx.compose.ui.unit.sp
import com.fynk.app.R

val provider = GoogleFont.Provider(
    providerAuthority = "com.google.android.gms.fonts",
    providerPackage = "com.google.android.gms",
    certificates = R.array.com_google_android_gms_fonts_certs
)

val PoppinsFont = GoogleFont("Poppins")
val InterFont = GoogleFont("Inter")

val PoppinsFontFamily = FontFamily(
    Font(googleFont = PoppinsFont, fontProvider = provider, weight = FontWeight.SemiBold),
    Font(googleFont = PoppinsFont, fontProvider = provider, weight = FontWeight.Medium)
)

val InterFontFamily = FontFamily(
    Font(googleFont = InterFont, fontProvider = provider, weight = FontWeight.Regular),
    Font(googleFont = InterFont, fontProvider = provider, weight = FontWeight.Medium)
)

val Typography = Typography(
    displayLarge = TextStyle(
        fontFamily = PoppinsFontFamily,
        fontWeight = FontWeight.SemiBold,
        fontSize = 57.sp,
        lineHeight = 64.sp,
        letterSpacing = (-0.25).sp
    ),
    headlineMedium = TextStyle(
        fontFamily = PoppinsFontFamily,
        fontWeight = FontWeight.SemiBold,
        fontSize = 28.sp,
        lineHeight = 36.sp,
        letterSpacing = 0.sp
    ),
    titleLarge = TextStyle(
        fontFamily = PoppinsFontFamily,
        fontWeight = FontWeight.Medium,
        fontSize = 20.sp,
        lineHeight = 28.sp,
        letterSpacing = 0.sp
    ),
    titleMedium = TextStyle(
        fontFamily = PoppinsFontFamily,
        fontWeight = FontWeight.Medium,
        fontSize = 16.sp,
        lineHeight = 24.sp,
        letterSpacing = 0.15.sp
    ),
    bodyLarge = TextStyle(
        fontFamily = InterFontFamily,
        fontWeight = FontWeight.Regular,
        fontSize = 16.sp,
        lineHeight = 24.sp,
        letterSpacing = 0.5.sp
    ),
    bodyMedium = TextStyle(
        fontFamily = InterFontFamily,
        fontWeight = FontWeight.Regular,
        fontSize = 14.sp,
        lineHeight = 20.sp,
        letterSpacing = 0.25.sp
    ),
    labelLarge = TextStyle(
        fontFamily = InterFontFamily,
        fontWeight = FontWeight.Medium,
        fontSize = 14.sp,
        lineHeight = 20.sp,
        letterSpacing = 0.1.sp
    ),
    labelSmall = TextStyle(
        fontFamily = InterFontFamily,
        fontWeight = FontWeight.Medium,
        fontSize = 12.sp,
        lineHeight = 16.sp,
        letterSpacing = 0.5.sp
    )
)
""",
    "data/datastore/ThemePreferenceRepository.kt": """package com.fynk.app.data.datastore

import android.content.Context
import androidx.datastore.core.DataStore
import androidx.datastore.preferences.core.Preferences
import androidx.datastore.preferences.core.edit
import androidx.datastore.preferences.core.stringPreferencesKey
import androidx.datastore.preferences.preferencesDataStore
import kotlinx.coroutines.flow.Flow
import kotlinx.coroutines.flow.map

enum class AppTheme {
    SKY, SLATE
}

val Context.dataStore: DataStore<Preferences> by preferencesDataStore(name = "settings")

class ThemePreferenceRepository(private val context: Context) {
    private val THEME_KEY = stringPreferencesKey("app_theme")

    val themeFlow: Flow<AppTheme> = context.dataStore.data.map { preferences ->
        val themeName = preferences[THEME_KEY] ?: AppTheme.SKY.name
        try {
            AppTheme.valueOf(themeName)
        } catch (e: Exception) {
            AppTheme.SKY
        }
    }

    suspend fun updateTheme(theme: AppTheme) {
        context.dataStore.edit { preferences ->
            preferences[THEME_KEY] = theme.name
        }
    }
}
""",
    "ui/theme/Theme.kt": """package com.fynk.app.ui.theme

import android.app.Activity
import androidx.compose.animation.animateColorAsState
import androidx.compose.animation.core.tween
import androidx.compose.foundation.isSystemInDarkTheme
import androidx.compose.material3.ColorScheme
import androidx.compose.material3.MaterialTheme
import androidx.compose.material3.darkColorScheme
import androidx.compose.material3.lightColorScheme
import androidx.compose.runtime.Composable
import androidx.compose.runtime.SideEffect
import androidx.compose.runtime.getValue
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.platform.LocalView
import androidx.core.view.WindowCompat
import com.fynk.app.data.datastore.AppTheme

private val SkyColorScheme = lightColorScheme(
    primary = SkyPrimary,
    primaryContainer = SkyPrimaryContainer,
    secondary = SkySecondary,
    background = SkyBackground,
    surface = SkySurface,
    onPrimary = SkyOnPrimary,
    onBackground = SkyOnBackground,
    onSurface = SkyOnBackground,
    error = SkyError,
    onError = Color.White
)

private val SlateColorScheme = darkColorScheme(
    primary = SlatePrimary,
    primaryContainer = SlatePrimaryContainer,
    secondary = SlateSecondary,
    background = SlateBackground,
    surface = SlateSurface,
    onPrimary = SlateOnPrimary,
    onBackground = SlateOnBackground,
    onSurface = SlateOnBackground,
    error = SlateError,
    onError = Color.Black
)

@Composable
fun animateColorScheme(targetColorScheme: ColorScheme): ColorScheme {
    val animationSpec = tween<Color>(durationMillis = 300)
    val primary by animateColorAsState(targetColorScheme.primary, animationSpec, label = "primary")
    val primaryContainer by animateColorAsState(targetColorScheme.primaryContainer, animationSpec, label = "primaryContainer")
    val secondary by animateColorAsState(targetColorScheme.secondary, animationSpec, label = "secondary")
    val background by animateColorAsState(targetColorScheme.background, animationSpec, label = "background")
    val surface by animateColorAsState(targetColorScheme.surface, animationSpec, label = "surface")
    val onPrimary by animateColorAsState(targetColorScheme.onPrimary, animationSpec, label = "onPrimary")
    val onBackground by animateColorAsState(targetColorScheme.onBackground, animationSpec, label = "onBackground")
    val onSurface by animateColorAsState(targetColorScheme.onSurface, animationSpec, label = "onSurface")
    val error by animateColorAsState(targetColorScheme.error, animationSpec, label = "error")
    val onError by animateColorAsState(targetColorScheme.onError, animationSpec, label = "onError")

    return ColorScheme(
        primary = primary,
        onPrimary = onPrimary,
        primaryContainer = primaryContainer,
        onPrimaryContainer = targetColorScheme.onPrimaryContainer,
        inversePrimary = targetColorScheme.inversePrimary,
        secondary = secondary,
        onSecondary = targetColorScheme.onSecondary,
        secondaryContainer = targetColorScheme.secondaryContainer,
        onSecondaryContainer = targetColorScheme.onSecondaryContainer,
        tertiary = targetColorScheme.tertiary,
        onTertiary = targetColorScheme.onTertiary,
        tertiaryContainer = targetColorScheme.tertiaryContainer,
        onTertiaryContainer = targetColorScheme.onTertiaryContainer,
        background = background,
        onBackground = onBackground,
        surface = surface,
        onSurface = onSurface,
        surfaceVariant = targetColorScheme.surfaceVariant,
        onSurfaceVariant = targetColorScheme.onSurfaceVariant,
        surfaceTint = targetColorScheme.surfaceTint,
        inverseSurface = targetColorScheme.inverseSurface,
        inverseOnSurface = targetColorScheme.inverseOnSurface,
        error = error,
        onError = onError,
        errorContainer = targetColorScheme.errorContainer,
        onErrorContainer = targetColorScheme.onErrorContainer,
        outline = targetColorScheme.outline,
        outlineVariant = targetColorScheme.outlineVariant,
        scrim = targetColorScheme.scrim,
        surfaceBright = targetColorScheme.surfaceBright,
        surfaceContainer = targetColorScheme.surfaceContainer,
        surfaceContainerHigh = targetColorScheme.surfaceContainerHigh,
        surfaceContainerHighest = targetColorScheme.surfaceContainerHighest,
        surfaceContainerLow = targetColorScheme.surfaceContainerLow,
        surfaceContainerLowest = targetColorScheme.surfaceContainerLowest,
        surfaceDim = targetColorScheme.surfaceDim,
    )
}

@Composable
fun FynkTheme(
    theme: AppTheme = AppTheme.SKY,
    content: @Composable () -> Unit
) {
    val targetColorScheme = when (theme) {
        AppTheme.SKY -> SkyColorScheme
        AppTheme.SLATE -> SlateColorScheme
    }

    val animatedColorScheme = animateColorScheme(targetColorScheme)
    val darkTheme = theme == AppTheme.SLATE

    val view = LocalView.current
    if (!view.isInEditMode) {
        SideEffect {
            val window = (view.context as Activity).window
            val windowCompat = WindowCompat.getInsetsController(window, view)
            windowCompat.isAppearanceLightStatusBars = !darkTheme
            windowCompat.isAppearanceLightNavigationBars = !darkTheme
        }
    }

    MaterialTheme(
        colorScheme = animatedColorScheme,
        typography = Typography,
        shapes = Shapes,
        content = content
    )
}
""",
    "MainActivity.kt": """package com.fynk.app

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
import com.fynk.app.data.datastore.ThemePreferenceRepository
import com.fynk.app.ui.theme.FynkTheme
import com.fynk.app.navigation.FynkNavHost

class MainActivity : ComponentActivity() {
    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        enableEdgeToEdge()
        val themeRepository = ThemePreferenceRepository(this)
        
        setContent {
            val theme by themeRepository.themeFlow.collectAsState(initial = AppTheme.SKY)
            
            FynkTheme(theme = theme) {
                Scaffold(modifier = Modifier.fillMaxSize()) { innerPadding ->
                    FynkNavHost(modifier = Modifier.padding(innerPadding))
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
