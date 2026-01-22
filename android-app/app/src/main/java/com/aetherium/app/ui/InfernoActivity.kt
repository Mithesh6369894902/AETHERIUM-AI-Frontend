package com.aetherium.app.ui

import android.os.Bundle
import android.widget.TextView
import androidx.appcompat.app.AppCompatActivity
import androidx.lifecycle.lifecycleScope
import com.aetherium.app.R
import com.aetherium.app.api.RetrofitClient
import kotlinx.coroutines.launch

class InfernoActivity : AppCompatActivity() {

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContentView(R.layout.activity_simple)

        val output = findViewById<TextView>(R.id.outputText)

        lifecycleScope.launch {
            val response = RetrofitClient.api.preprocess(
                listOf(mapOf("a" to 1, "b" to 2))
            )
            if (response.isSuccessful) {
                output.text = response.body().toString()
            }
        }
    }
}
