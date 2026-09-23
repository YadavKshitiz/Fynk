package com.fynk.app.ui.theme

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
