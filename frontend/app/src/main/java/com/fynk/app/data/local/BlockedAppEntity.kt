package com.fynk.app.data.local

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
