package com.fynk.app.domain

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
