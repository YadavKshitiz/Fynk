package com.fynk.app

import android.os.Bundle
import androidx.activity.ComponentActivity
import androidx.activity.compose.setContent
import androidx.activity.enableEdgeToEdge
import androidx.compose.foundation.layout.fillMaxSize
import androidx.compose.foundation.layout.padding
import androidx.compose.material3.Scaffold
import androidx.compose.ui.Modifier
import com.fynk.app.ui.theme.FynkTheme
import com.fynk.app.navigation.FynkNavHost

class MainActivity : ComponentActivity() {
    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        enableEdgeToEdge()
        setContent {
            FynkTheme {
                Scaffold(modifier = Modifier.fillMaxSize()) { innerPadding ->
                    FynkNavHost(modifier = Modifier.padding(innerPadding))
                }
            }
        }
    }
}
