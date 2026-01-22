package com.aetherium.app.ui

import android.os.Bundle
import android.widget.TextView
import androidx.appcompat.app.AppCompatActivity
import androidx.lifecycle.lifecycleScope
import com.aetherium.app.R
import com.aetherium.app.api.RetrofitClient
import kotlinx.coroutines.launch

class ModelCraftActivity : AppCompatActivity() {

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContentView(R.layout.activity_simple)

        val output = findViewById<TextView>(R.id.outputText)

        lifecycleScope.launch {
            val res = RetrofitClient.api.benchmark(
                mapOf(
                    "data" to emptyList<Map<String, Any>>(),
                    "target" to "label"
                )
            )
            if (res.isSuccessful) {
                output.text = res.body().toString()
            }
        }
    }
}
