package com.fynk.app.data.local

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
