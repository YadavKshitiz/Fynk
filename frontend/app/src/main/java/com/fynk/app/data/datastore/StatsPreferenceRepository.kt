package com.fynk.app.data.datastore

import android.content.Context
import androidx.datastore.preferences.core.edit
import androidx.datastore.preferences.core.intPreferencesKey
import androidx.datastore.preferences.core.stringPreferencesKey
import com.fynk.app.domain.StreakCalculator
import kotlinx.coroutines.flow.Flow
import kotlinx.coroutines.flow.map

class StatsPreferenceRepository(private val context: Context) {
    private val CURRENT_STREAK_KEY = intPreferencesKey("current_streak")
    private val LAST_STREAK_UPDATE_DATE_KEY = stringPreferencesKey("last_streak_update_date")

    val currentStreakFlow: Flow<Int> = context.dataStore.data.map { it[CURRENT_STREAK_KEY] ?: 0 }
    val lastStreakUpdateDateFlow: Flow<String?> = context.dataStore.data.map { it[LAST_STREAK_UPDATE_DATE_KEY] }

    suspend fun updateStreakOnDayRollover(todayDateString: String) {
        context.dataStore.edit { preferences ->
            val currentStreak = preferences[CURRENT_STREAK_KEY] ?: 0
            val lastDate = preferences[LAST_STREAK_UPDATE_DATE_KEY]
            
            val newStats = StreakCalculator.calculateStreakOnDayRollover(
                currentStreak, lastDate, todayDateString
            )
            
            preferences[CURRENT_STREAK_KEY] = newStats.first
            preferences[LAST_STREAK_UPDATE_DATE_KEY] = newStats.second
        }
    }

    suspend fun resetStreakOnPasswordUse(todayDateString: String) {
        context.dataStore.edit { preferences ->
            preferences[CURRENT_STREAK_KEY] = 0
            preferences[LAST_STREAK_UPDATE_DATE_KEY] = todayDateString
        }
    }
}
