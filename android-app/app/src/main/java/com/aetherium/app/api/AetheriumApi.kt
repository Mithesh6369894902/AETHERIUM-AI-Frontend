package com.aetherium.app.api

import retrofit2.Response
import retrofit2.http.*

interface AetheriumApi {

    @POST("text/sentiment")
    suspend fun sentiment(
        @Body payload: Map<String, String>
    ): Response<Map<String, String>>

    @POST("modelcraft/benchmark")
    suspend fun benchmark(
        @Body payload: Map<String, Any>
    ): Response<Map<String, Any>>

    @Multipart
    @POST("vision/edges")
    suspend fun detectEdges(
        @Part file: MultipartBody.Part,
        @Part("t1") t1: Int,
        @Part("t2") t2: Int
    ): Response<ResponseBody>
}
