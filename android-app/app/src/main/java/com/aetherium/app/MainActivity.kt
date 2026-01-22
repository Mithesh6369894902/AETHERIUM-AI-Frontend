package com.aetherium.app

import android.content.Intent
import android.os.Bundle
import android.widget.Button
import androidx.appcompat.app.AppCompatActivity
import com.aetherium.app.ui.*

class MainActivity : AppCompatActivity() {

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContentView(R.layout.activity_main)

        findViewById<Button>(R.id.btnInferno).setOnClickListener {
            startActivity(Intent(this, InfernoActivity::class.java))
        }

        findViewById<Button>(R.id.btnText).setOnClickListener {
            startActivity(Intent(this, TextVortexActivity::class.java))
        }

        findViewById<Button>(R.id.btnVision).setOnClickListener {
            startActivity(Intent(this, VisionBlazeActivity::class.java))
        }

        findViewById<Button>(R.id.btnAlpha).setOnClickListener {
            startActivity(Intent(this, AlphaFluxActivity::class.java))
        }

        findViewById<Button>(R.id.btnModel).setOnClickListener {
            startActivity(Intent(this, ModelCraftActivity::class.java))
        }
    }
}
