#include "raylib.h"
#include "raymath.h"

/*
 * Ornek 02 - 3D Kureler Sahnesi
 *
 * Kitaptaki sahneyi raylib'in 3D fonksiyonlari ile olusturur.
 * 3 kure: Kirmizi (0,-1,3), Mavi (2,0,4), Yesil (-2,0,4)
 * Fare ile kamerayi dondurebilirsiniz.
 */
int main(void)
{
    const int screenWidth = 800;
    const int screenHeight = 600;

    InitWindow(screenWidth, screenHeight, "Ornek 02 - 3D Kureler Sahnesi");

    // Kamera tanimla
    Camera3D camera = { 0 };
    camera.position = (Vector3){ 0.0f, 2.0f, -6.0f };
    camera.target = (Vector3){ 0.0f, 0.0f, 3.0f };
    camera.up = (Vector3){ 0.0f, 1.0f, 0.0f };
    camera.fovy = 53.0f;   // Kitaptaki yaklasik FOV degeri
    camera.projection = CAMERA_PERSPECTIVE;

    SetTargetFPS(60);

    while (!WindowShouldClose())
    {
        UpdateCamera(&camera, CAMERA_ORBITAL);

        BeginDrawing();
            ClearBackground(RAYWHITE);

            BeginMode3D(camera);
                // Kitaptaki 3 kure
                DrawSphere((Vector3){ 0.0f, -1.0f, 3.0f }, 1.0f, RED);
                DrawSphere((Vector3){ 2.0f,  0.0f, 4.0f }, 1.0f, BLUE);
                DrawSphere((Vector3){-2.0f,  0.0f, 4.0f }, 1.0f, GREEN);

                // Buyuk zemin kuresi
                DrawSphere((Vector3){ 0.0f, -5001.0f, 0.0f }, 5000.0f, YELLOW);

                // Koordinat eksenleri
                DrawLine3D((Vector3){0, 0, 0}, (Vector3){3, 0, 0}, RED);    // X ekseni
                DrawLine3D((Vector3){0, 0, 0}, (Vector3){0, 3, 0}, GREEN);  // Y ekseni
                DrawLine3D((Vector3){0, 0, 0}, (Vector3){0, 0, 3}, BLUE);   // Z ekseni

                DrawGrid(10, 1.0f);
            EndMode3D();

            DrawText("3D Kureler Sahnesi", 10, 10, 20, DARKGRAY);
            DrawText("Fare ile kamerayi dondur", 10, 35, 16, GRAY);
            DrawText("Kirmizi: (0,-1,3) r=1", 10, screenHeight - 60, 14, RED);
            DrawText("Mavi:    (2, 0,4) r=1", 10, screenHeight - 42, 14, BLUE);
            DrawText("Yesil:  (-2, 0,4) r=1", 10, screenHeight - 24, 14, GREEN);
        EndDrawing();
    }

    CloseWindow();
    return 0;
}
