package com.fynk.app.data.repository

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
