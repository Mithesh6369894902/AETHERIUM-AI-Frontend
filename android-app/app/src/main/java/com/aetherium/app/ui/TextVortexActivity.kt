package com.aetherium.app.ui

import android.os.Bundle
import android.widget.Button
import android.widget.EditText
import android.widget.TextView
import androidx.appcompat.app.AppCompatActivity
import androidx.lifecycle.lifecycleScope
import com.aetherium.app.R
import com.aetherium.app.api.RetrofitClient
import kotlinx.coroutines.launch

class TextVortexActivity : AppCompatActivity() {

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContentView(R.layout.activity_text)

        val input = findViewById<EditText>(R.id.inputText)
        val button = findViewById<Button>(R.id.actionBtn)
        val output = findViewById<TextView>(R.id.outputText)

        button.setOnClickListener {
            lifecycleScope.launch {
                val res = RetrofitClient.api.sentiment(
                    mapOf("text" to input.text.toString())
                )
                if (res.isSuccessful) {
                    output.text = res.body()?.get("sentiment")
                }
            }
        }
    }
}
