#include "raylib.h"

/*
 * Ornek 01 - Temel Raylib Penceresi ve Piksel Cizimi
 *
 * Bu program raylib ile temel bir pencere olusturur ve
 * piksel piksel cizim yapar. Isin izleme (ray tracing)
 * de temelde ayni seyi yapar: her piksel icin bir renk
 * hesaplar ve o pikseli boyar.
 */
int main(void)
{
    const int screenWidth = 800;
    const int screenHeight = 600;

    InitWindow(screenWidth, screenHeight, "Ornek 01 - Temel Raylib Penceresi");
    SetTargetFPS(60);

    while (!WindowShouldClose())
    {
        BeginDrawing();
            ClearBackground(RAYWHITE);

            // Piksel piksel cizim ornegi - renk gradyani
            for (int i = 0; i < 100; i++)
            {
                for (int j = 0; j < 100; j++)
                {
                    Color color = {
                        (unsigned char)(i * 2.55f),
                        (unsigned char)(j * 2.55f),
                        128, 255
                    };
                    DrawPixel(350 + i, 250 + j, color);
                }
            }

            DrawText("Merhaba Bilgisayar Grafikleri!", 250, 200, 24, DARKGRAY);
            DrawText("Piksel piksel cizim ornegi (100x100)", 260, 380, 18, GRAY);
        EndDrawing();
    }

    CloseWindow();
    return 0;
}
