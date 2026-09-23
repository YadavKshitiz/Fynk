import os

base_dir = "/home/yadavkshitiz/Android/Fynk/frontend"

files = {
    "app/src/main/java/com/fynk/app/data/local/BlockedAppEntity.kt": """package com.fynk.app.data.local

import androidx.room.Entity
import androidx.room.PrimaryKey

@Entity(tableName = "blocked_apps")
data class BlockedAppEntity(
    @PrimaryKey
    val packageName: String,
    val appName: String,
    val limitType: String, // "HOURLY" or "DAILY"
    val limitMinutes: Int,
    val windowStartTimestamp: Long,
    val minutesUsedInWindow: Int,
    val openCountToday: Int,
    val dateOfOpenCount: String,
    val isCurrentlyBlocked: Boolean
)
""",
    "app/src/main/java/com/fynk/app/data/local/BlockedAppDao.kt": """package com.fynk.app.data.local

import androidx.room.Dao
import androidx.room.Insert
import androidx.room.OnConflictStrategy
import androidx.room.Query
import kotlinx.coroutines.flow.Flow

@Dao
interface BlockedAppDao {
    @Query("SELECT * FROM blocked_apps")
    fun getAll(): Flow<List<BlockedAppEntity>>

    @Query("SELECT * FROM blocked_apps WHERE packageName = :packageName")
    suspend fun getByPackageName(packageName: String): BlockedAppEntity?

    @Insert(onConflict = OnConflictStrategy.REPLACE)
    suspend fun insertOrUpdate(app: BlockedAppEntity)

    @Query("DELETE FROM blocked_apps WHERE packageName = :packageName")
    suspend fun delete(packageName: String)

    @Query("UPDATE blocked_apps SET windowStartTimestamp = :windowStartTimestamp, minutesUsedInWindow = :minutesUsedInWindow, openCountToday = :openCountToday, dateOfOpenCount = :dateOfOpenCount, isCurrentlyBlocked = :isCurrentlyBlocked WHERE packageName = :packageName")
    suspend fun updateUsageState(
        packageName: String,
        windowStartTimestamp: Long,
        minutesUsedInWindow: Int,
        openCountToday: Int,
        dateOfOpenCount: String,
        isCurrentlyBlocked: Boolean
    )
}
""",
    "app/src/main/java/com/fynk/app/data/local/FynkDatabase.kt": """package com.fynk.app.data.local

import android.content.Context
import androidx.room.Database
import androidx.room.Room
import androidx.room.RoomDatabase

@Database(
    entities = [BlockedAppEntity::class],
    version = 1,
    exportSchema = true
)
abstract class FynkDatabase : RoomDatabase() {
    abstract fun blockedAppDao(): BlockedAppDao

    companion object {
        @Volatile
        private var INSTANCE: FynkDatabase? = null

        fun getInstance(context: Context): FynkDatabase {
            return INSTANCE ?: synchronized(this) {
                val instance = Room.databaseBuilder(
                    context.applicationContext,
                    FynkDatabase::class.java,
                    "fynk_database"
                )
                // .addMigrations(...)
                .build()
                INSTANCE = instance
                instance
            }
        }
    }
}
""",
    "app/src/main/java/com/fynk/app/domain/LimitCalculator.kt": """package com.fynk.app.domain

import com.fynk.app.data.local.BlockedAppEntity
import java.time.Instant
import java.time.ZoneId
import java.time.format.DateTimeFormatter

data class RemainingState(
    val isBlocked: Boolean,
    val minutesRemaining: Int,
    val resetsAtTimestamp: Long
)

object LimitCalculator {
    fun calculateRemainingState(app: BlockedAppEntity, now: Long): RemainingState {
        val todayStr = getLocalDateString(now)
        
        return if (app.limitType == "DAILY") {
            if (app.dateOfOpenCount != todayStr) {
                // Fresh day
                RemainingState(
                    isBlocked = false,
                    minutesRemaining = app.limitMinutes,
                    resetsAtTimestamp = getNextMidnight(now)
                )
            } else {
                val remaining = (app.limitMinutes - app.minutesUsedInWindow).coerceAtLeast(0)
                RemainingState(
                    isBlocked = remaining <= 0,
                    minutesRemaining = remaining,
                    resetsAtTimestamp = getNextMidnight(now)
                )
            }
        } else {
            // HOURLY
            if (now - app.windowStartTimestamp >= 60 * 60 * 1000L) {
                // Window expired
                RemainingState(
                    isBlocked = false,
                    minutesRemaining = app.limitMinutes,
                    resetsAtTimestamp = now
                )
            } else {
                val remaining = (app.limitMinutes - app.minutesUsedInWindow).coerceAtLeast(0)
                RemainingState(
                    isBlocked = remaining <= 0,
                    minutesRemaining = remaining,
                    resetsAtTimestamp = app.windowStartTimestamp + 60 * 60 * 1000L
                )
            }
        }
    }

    private fun getLocalDateString(timestamp: Long): String {
        return Instant.ofEpochMilli(timestamp)
            .atZone(ZoneId.systemDefault())
            .format(DateTimeFormatter.ofPattern("yyyy-MM-dd"))
    }

    private fun getNextMidnight(timestamp: Long): Long {
        val zdt = Instant.ofEpochMilli(timestamp).atZone(ZoneId.systemDefault())
        val nextMidnight = zdt.toLocalDate().plusDays(1).atStartOfDay(zdt.zone)
        return nextMidnight.toInstant().toEpochMilli()
    }
}
""",
    "app/src/main/java/com/fynk/app/data/repository/BlockedAppRepository.kt": """package com.fynk.app.data.repository

import com.fynk.app.data.local.BlockedAppDao
import com.fynk.app.data.local.BlockedAppEntity
import com.fynk.app.domain.LimitCalculator
import com.fynk.app.domain.RemainingState
import kotlinx.coroutines.flow.Flow

class BlockedAppRepository(private val dao: BlockedAppDao) {
    fun getAll(): Flow<List<BlockedAppEntity>> = dao.getAll()
    
    suspend fun getByPackageName(packageName: String): BlockedAppEntity? {
        return dao.getByPackageName(packageName)
    }
    
    suspend fun insertOrUpdate(app: BlockedAppEntity) {
        dao.insertOrUpdate(app)
    }
    
    suspend fun delete(packageName: String) {
        dao.delete(packageName)
    }
    
    suspend fun updateUsageState(
        packageName: String,
        windowStartTimestamp: Long,
        minutesUsedInWindow: Int,
        openCountToday: Int,
        dateOfOpenCount: String,
        isCurrentlyBlocked: Boolean
    ) {
        dao.updateUsageState(
            packageName, windowStartTimestamp, minutesUsedInWindow, 
            openCountToday, dateOfOpenCount, isCurrentlyBlocked
        )
    }
    
    fun calculateRemainingState(app: BlockedAppEntity, now: Long): RemainingState {
        return LimitCalculator.calculateRemainingState(app, now)
    }
}
""",
    "app/src/main/java/com/fynk/app/domain/StreakCalculator.kt": """package com.fynk.app.domain

import java.time.LocalDate
import java.time.format.DateTimeFormatter
import java.time.temporal.ChronoUnit

object StreakCalculator {
    fun calculateStreakOnDayRollover(currentStreak: Int, lastUpdateDate: String?, todayDateString: String): Pair<Int, String> {
        if (lastUpdateDate == null) {
            return Pair(1, todayDateString)
        }
        
        if (lastUpdateDate == todayDateString) {
            return Pair(currentStreak, todayDateString)
        }
        
        val formatter = DateTimeFormatter.ofPattern("yyyy-MM-dd")
        val lastDate = try { LocalDate.parse(lastUpdateDate, formatter) } catch (e: Exception) { null }
        val todayDate = try { LocalDate.parse(todayDateString, formatter) } catch (e: Exception) { null }
        
        if (lastDate != null && todayDate != null) {
            val daysBetween = ChronoUnit.DAYS.between(lastDate, todayDate)
            if (daysBetween >= 1L) {
                return Pair(currentStreak + daysBetween.toInt(), todayDateString)
            }
        }
        
        return Pair(currentStreak, todayDateString)
    }
}
""",
    "app/src/main/java/com/fynk/app/data/datastore/StatsPreferenceRepository.kt": """package com.fynk.app.data.datastore

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
"""
}

for path, content in files.items():
    full_path = os.path.join(base_dir, path)
    os.makedirs(os.path.dirname(full_path), exist_ok=True)
    with open(full_path, "w") as f:
        f.write(content)

print("Files created.")
