package com.fynk.app.domain

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
