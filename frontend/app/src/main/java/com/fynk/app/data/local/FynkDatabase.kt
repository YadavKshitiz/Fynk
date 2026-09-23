package com.fynk.app.data.local

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
