#include "raylib.h"

/*
 * Ornek 10 - 2D Kamera ve Dunya
 * Derleme: cc -o ornek10 ornek10_2d_kamera.c -lraylib -lm
 */

#define BINA_SAYISI 50

int main(void)
{
    const int W = 900, H = 600;
    InitWindow(W, H, "Ornek 10 - 2D Kamera ve Dunya");
    SetTargetFPS(60);

    Rectangle oyuncu = { 400, 280, 30, 50 };
    float oyuncuHiz = 5.0f;

    Rectangle binalar[BINA_SAYISI];
    Color binaRenkleri[BINA_SAYISI];
    int ofs = 0;
    for (int i = 0; i < BINA_SAYISI; i++) {
        int en = GetRandomValue(60, 160);
        int boy = GetRandomValue(80, 350);
        binalar[i] = (Rectangle){ ofs - 4000, H - 100 - boy, en, boy };
        binaRenkleri[i] = (Color){ GetRandomValue(120,250), GetRandomValue(120,250), GetRandomValue(120,250), 255 };
        ofs += en + GetRandomValue(2, 12);
    }

    Camera2D kamera = { 0 };
    kamera.target = (Vector2){ oyuncu.x + 15, oyuncu.y + 25 };
    kamera.offset = (Vector2){ W/2.0f, H/2.0f };
    kamera.zoom = 1.0f;

    while (!WindowShouldClose())
    {
        if (IsKeyDown(KEY_RIGHT) || IsKeyDown(KEY_D)) oyuncu.x += oyuncuHiz;
        if (IsKeyDown(KEY_LEFT)  || IsKeyDown(KEY_A)) oyuncu.x -= oyuncuHiz;
        if (IsKeyDown(KEY_UP)    || IsKeyDown(KEY_W)) oyuncu.y -= oyuncuHiz;
        if (IsKeyDown(KEY_DOWN)  || IsKeyDown(KEY_S)) oyuncu.y += oyuncuHiz;

        kamera.target = (Vector2){ oyuncu.x + 15, oyuncu.y + 25 };
        if (IsKeyDown(KEY_Q)) kamera.rotation -= 1.5f;
        if (IsKeyDown(KEY_E)) kamera.rotation += 1.5f;
        if (IsKeyPressed(KEY_R)) kamera.rotation = 0.0f;
        kamera.zoom += GetMouseWheelMove() * 0.15f;
        if (kamera.zoom < 0.2f) kamera.zoom = 0.2f;
        if (kamera.zoom > 5.0f) kamera.zoom = 5.0f;

        BeginDrawing();
            ClearBackground((Color){200, 220, 240, 255});
            BeginMode2D(kamera);
                DrawRectangle(-5000, H - 100, 10000, 200, DARKGREEN);
                for (int i = 0; i < BINA_SAYISI; i++) {
                    DrawRectangleRec(binalar[i], binaRenkleri[i]);
                    for (int py = (int)binalar[i].y + 10; py < (int)(binalar[i].y + binalar[i].height - 15); py += 20)
                        for (int px = (int)binalar[i].x + 8; px < (int)(binalar[i].x + binalar[i].width - 15); px += 18)
                            DrawRectangle(px, py, 10, 12, Fade(YELLOW, 0.6f));
                }
                DrawRectangleRec(oyuncu, RED);
                DrawRectangleLinesEx(oyuncu, 2, MAROON);
            EndMode2D();

            DrawRectangle(0, 0, W, 48, Fade(BLACK, 0.7f));
            DrawText("2D Kamera ve Dunya", 15, 12, 22, WHITE);
            DrawRectangle(5, 55, 290, 140, Fade(WHITE, 0.85f));
            DrawText(TextFormat("target  = (%.0f, %.0f)", kamera.target.x, kamera.target.y), 15, 62, 13, GRAY);
            DrawText(TextFormat("offset  = (%.0f, %.0f)", kamera.offset.x, kamera.offset.y), 15, 80, 13, GRAY);
            DrawText(TextFormat("zoom    = %.2f", kamera.zoom), 15, 98, 13, GRAY);
            DrawText(TextFormat("rotation= %.1f", kamera.rotation), 15, 116, 13, GRAY);
            DrawText("WASD:tasi Q/E:don Scroll:zoom", 15, 140, 12, DARKGREEN);

            Vector2 fareD = GetScreenToWorld2D(GetMousePosition(), kamera);
            DrawText(TextFormat("Fare dunya: (%.0f, %.0f)", fareD.x, fareD.y), W - 280, H - 28, 12, DARKBLUE);
        EndDrawing();
    }
    CloseWindow();
    return 0;
}
