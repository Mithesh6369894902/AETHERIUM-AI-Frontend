package com.aetherium.app.ui

import android.os.Bundle
import android.widget.TextView
import androidx.appcompat.app.AppCompatActivity
import androidx.lifecycle.lifecycleScope
import com.aetherium.app.R
import com.aetherium.app.api.RetrofitClient
import kotlinx.coroutines.launch

class AlphaFluxActivity : AppCompatActivity() {

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContentView(R.layout.activity_simple)

        val output = findViewById<TextView>(R.id.outputText)

        lifecycleScope.launch {
            val res = RetrofitClient.api.forecast(
                mapOf(
                    "symbol" to "AAPL",
                    "start_date" to "2020-01-01",
                    "end_date" to "2024-01-01",
                    "horizon" to 10
                )
            )
            if (res.isSuccessful) {
                output.text = res.body().toString()
            }
        }
    }
}
