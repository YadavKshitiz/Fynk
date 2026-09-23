package com.fynk.app.data.datastore

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
