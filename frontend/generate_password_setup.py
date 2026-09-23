import os

base_dir = "/home/yadavkshitiz/Android/Fynk/frontend"

files = {
    "app/src/main/java/com/fynk/app/util/SecurityUtil.kt": """package com.fynk.app.util

import android.util.Base64
import java.security.MessageDigest
import java.security.SecureRandom

object SecurityUtil {
    fun generateSalt(): String {
        val random = SecureRandom()
        val salt = ByteArray(16)
        random.nextBytes(salt)
        return Base64.encodeToString(salt, Base64.NO_WRAP)
    }

    fun hashPassword(password: String, salt: String): String {
        val md = MessageDigest.getInstance("SHA-256")
        md.update(Base64.decode(salt, Base64.NO_WRAP))
        val hashedBytes = md.digest(password.toByteArray(Charsets.UTF_8))
        return Base64.encodeToString(hashedBytes, Base64.NO_WRAP)
    }
}
""",
    "app/src/main/java/com/fynk/app/data/datastore/SecurityPreferenceRepository.kt": """package com.fynk.app.data.datastore

import android.content.Context
import androidx.datastore.preferences.core.booleanPreferencesKey
import androidx.datastore.preferences.core.edit
import androidx.datastore.preferences.core.intPreferencesKey
import androidx.datastore.preferences.core.stringPreferencesKey
import kotlinx.coroutines.flow.Flow
import kotlinx.coroutines.flow.map

class SecurityPreferenceRepository(private val context: Context) {
    private val FRIEND_NAME_KEY = stringPreferencesKey("friend_name")
    private val PASSWORD_HASH_KEY = stringPreferencesKey("password_hash")
    private val UNLOCK_DURATION_KEY = intPreferencesKey("unlock_duration_minutes")
    private val SETUP_COMPLETE_KEY = booleanPreferencesKey("is_password_setup_complete")

    val isPasswordSetupCompleteFlow: Flow<Boolean> = context.dataStore.data.map { preferences ->
        preferences[SETUP_COMPLETE_KEY] ?: false
    }

    suspend fun saveSecuritySettings(
        friendName: String,
        passwordHash: String, // "salt:hash"
        unlockDurationMinutes: Int
    ) {
        context.dataStore.edit { preferences ->
            preferences[FRIEND_NAME_KEY] = friendName
            preferences[PASSWORD_HASH_KEY] = passwordHash
            preferences[UNLOCK_DURATION_KEY] = unlockDurationMinutes
            preferences[SETUP_COMPLETE_KEY] = true
        }
    }
}
""",
    "app/src/main/java/com/fynk/app/ui/screens/passwordsetup/PasswordSetupScreen.kt": """package com.fynk.app.ui.screens.passwordsetup

import androidx.compose.animation.core.Animatable
import androidx.compose.animation.core.keyframes
import androidx.compose.foundation.horizontalScroll
import androidx.compose.foundation.layout.*
import androidx.compose.foundation.rememberScrollState
import androidx.compose.foundation.text.KeyboardOptions
import androidx.compose.foundation.verticalScroll
import androidx.compose.material.icons.Icons
import androidx.compose.material.icons.filled.Visibility
import androidx.compose.material.icons.filled.VisibilityOff
import androidx.compose.material3.*
import androidx.compose.runtime.*
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.graphics.graphicsLayer
import androidx.compose.ui.platform.LocalContext
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.text.input.KeyboardType
import androidx.compose.ui.text.input.PasswordVisualTransformation
import androidx.compose.ui.text.input.VisualTransformation
import androidx.compose.ui.unit.dp
import com.fynk.app.data.datastore.SecurityPreferenceRepository
import com.fynk.app.util.SecurityUtil
import kotlinx.coroutines.launch

@Composable
fun PasswordSetupScreen(
    onSaveComplete: () -> Unit = {}
) {
    val context = LocalContext.current
    val coroutineScope = rememberCoroutineScope()
    val securityRepository = remember { SecurityPreferenceRepository(context) }

    var friendName by remember { mutableStateOf("") }
    var password by remember { mutableStateOf("") }
    var confirmPassword by remember { mutableStateOf("") }
    var isPasswordVisible by remember { mutableStateOf(false) }

    var selectedDuration by remember { mutableStateOf<Int?>(60) }
    var customDurationText by remember { mutableStateOf("") }

    var nameError by remember { mutableStateOf<String?>(null) }
    var passwordError by remember { mutableStateOf<String?>(null) }
    var confirmError by remember { mutableStateOf<String?>(null) }

    val shakeAnim = remember { Animatable(0f) }

    val effectiveDuration = selectedDuration ?: customDurationText.toIntOrNull()?.coerceIn(1, 1440) ?: 60

    fun validateAndSave() {
        nameError = null
        passwordError = null
        confirmError = null
        var isValid = true

        if (friendName.isBlank()) {
            nameError = "Friend's name cannot be empty"
            isValid = false
        }
        if (password.length < 4) {
            passwordError = "Password must be at least 4 characters"
            isValid = false
        }
        if (password != confirmPassword) {
            confirmError = "Passwords do not match"
            isValid = false
            coroutineScope.launch {
                shakeAnim.animateTo(
                    targetValue = 0f,
                    animationSpec = keyframes {
                        durationMillis = 300
                        0f at 0
                        20f at 50
                        -20f at 100
                        20f at 150
                        -20f at 200
                        10f at 250
                        0f at 300
                    }
                )
            }
        }

        if (isValid) {
            coroutineScope.launch {
                val salt = SecurityUtil.generateSalt()
                val hash = SecurityUtil.hashPassword(password, salt)
                val storedValue = "$salt:$hash"
                securityRepository.saveSecuritySettings(
                    friendName = friendName.trim(),
                    passwordHash = storedValue,
                    unlockDurationMinutes = effectiveDuration
                )
                onSaveComplete()
            }
        }
    }

    Column(
        modifier = Modifier
            .fillMaxSize()
            .padding(24.dp)
            .verticalScroll(rememberScrollState()),
        horizontalAlignment = Alignment.Start
    ) {
        Spacer(modifier = Modifier.height(32.dp))

        Text(
            text = "Set up your accountability partner",
            style = MaterialTheme.typography.headlineMedium,
            color = MaterialTheme.colorScheme.onBackground
        )

        Spacer(modifier = Modifier.height(8.dp))

        Text(
            text = "Hand your phone to your trusted friend now — they'll set a password only they know.",
            style = MaterialTheme.typography.bodyMedium,
            color = MaterialTheme.colorScheme.onBackground.copy(alpha = 0.7f)
        )

        Spacer(modifier = Modifier.height(32.dp))

        Card(
            modifier = Modifier
                .fillMaxWidth()
                .graphicsLayer {
                    translationX = shakeAnim.value
                },
            shape = MaterialTheme.shapes.large,
            colors = CardDefaults.cardColors(containerColor = MaterialTheme.colorScheme.surfaceVariant)
        ) {
            Column(
                modifier = Modifier
                    .fillMaxWidth()
                    .padding(16.dp)
            ) {
                OutlinedTextField(
                    value = friendName,
                    onValueChange = { friendName = it; nameError = null },
                    label = { Text("Friend's name") },
                    isError = nameError != null,
                    supportingText = nameError?.let { { Text(it) } },
                    singleLine = true,
                    modifier = Modifier.fillMaxWidth()
                )

                Spacer(modifier = Modifier.height(16.dp))

                OutlinedTextField(
                    value = password,
                    onValueChange = { password = it; passwordError = null },
                    label = { Text("Set password") },
                    isError = passwordError != null,
                    supportingText = passwordError?.let { { Text(it) } },
                    singleLine = true,
                    visualTransformation = if (isPasswordVisible) VisualTransformation.None else PasswordVisualTransformation(),
                    keyboardOptions = KeyboardOptions(keyboardType = KeyboardType.Password),
                    trailingIcon = {
                        IconButton(onClick = { isPasswordVisible = !isPasswordVisible }) {
                            Icon(
                                imageVector = if (isPasswordVisible) Icons.Default.Visibility else Icons.Default.VisibilityOff,
                                contentDescription = if (isPasswordVisible) "Hide password" else "Show password"
                            )
                        }
                    },
                    modifier = Modifier.fillMaxWidth()
                )

                Spacer(modifier = Modifier.height(16.dp))

                OutlinedTextField(
                    value = confirmPassword,
                    onValueChange = { confirmPassword = it; confirmError = null },
                    label = { Text("Confirm password") },
                    isError = confirmError != null,
                    supportingText = confirmError?.let { { Text(it, color = MaterialTheme.colorScheme.error) } },
                    singleLine = true,
                    visualTransformation = if (isPasswordVisible) VisualTransformation.None else PasswordVisualTransformation(),
                    keyboardOptions = KeyboardOptions(keyboardType = KeyboardType.Password),
                    modifier = Modifier.fillMaxWidth()
                )
            }
        }

        Spacer(modifier = Modifier.height(32.dp))

        Text(
            text = "Unlock session length",
            style = MaterialTheme.typography.titleMedium,
            color = MaterialTheme.colorScheme.onBackground
        )

        Spacer(modifier = Modifier.height(8.dp))

        Row(
            modifier = Modifier
                .fillMaxWidth()
                .horizontalScroll(rememberScrollState()),
            horizontalArrangement = Arrangement.spacedBy(8.dp)
        ) {
            val presets = listOf(15 to "15 min", 30 to "30 min", 60 to "1 hour", 120 to "2 hours")
            presets.forEach { (minutes, label) ->
                FilterChip(
                    selected = selectedDuration == minutes,
                    onClick = {
                        selectedDuration = minutes
                        customDurationText = ""
                    },
                    label = { Text(label) }
                )
            }
        }

        Spacer(modifier = Modifier.height(8.dp))

        OutlinedTextField(
            value = customDurationText,
            onValueChange = { newValue ->
                val filtered = newValue.filter { it.isDigit() }
                customDurationText = filtered
                if (filtered.isNotEmpty()) {
                    selectedDuration = null
                }
            },
            label = { Text("Custom minutes") },
            keyboardOptions = KeyboardOptions(keyboardType = KeyboardType.Number),
            singleLine = true,
            modifier = Modifier.width(200.dp)
        )

        Spacer(modifier = Modifier.height(8.dp))

        Text(
            text = "Currently: $effectiveDuration minutes",
            style = MaterialTheme.typography.bodySmall,
            color = MaterialTheme.colorScheme.onBackground.copy(alpha = 0.5f)
        )

        Spacer(modifier = Modifier.height(48.dp))

        Button(
            onClick = { validateAndSave() },
            modifier = Modifier
                .fillMaxWidth()
                .height(56.dp),
            shape = MaterialTheme.shapes.large
        ) {
            Text(
                text = "Save",
                style = MaterialTheme.typography.titleMedium.copy(fontWeight = FontWeight.SemiBold)
            )
        }

        Spacer(modifier = Modifier.height(32.dp))
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
