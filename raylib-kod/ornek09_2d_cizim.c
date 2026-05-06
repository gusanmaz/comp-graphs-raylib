#include "raylib.h"
#include <math.h>

/*
 * Ornek 09 - 2D Cizim ve Sekiller
 * Derleme: cc -o ornek09 ornek09_2d_cizim.c -lraylib -lm
 */

int main(void)
{
    const int W = 950, H = 650;
    InitWindow(W, H, "Ornek 09 - 2D Cizim ve Sekiller");
    SetTargetFPS(60);
    int frame = 0;

    Vector2 dairePos = { 700.0f, 500.0f };
    float daireR = 30.0f;
    Rectangle sabitKutu = { 600, 460, 120, 80 };
    bool carpisiyor = false;

    Image img = GenImageChecked(64, 64, 8, 8, ORANGE, WHITE);
    Texture2D doku = LoadTextureFromImage(img);
    UnloadImage(img);

    while (!WindowShouldClose())
    {
        frame++;
        float t = frame * 0.03f;
        dairePos = GetMousePosition();
        carpisiyor = CheckCollisionCircleRec(dairePos, daireR, sabitKutu);

        BeginDrawing();
        ClearBackground(RAYWHITE);
        DrawRectangle(0, 0, W, 45, Fade(DARKBLUE, 0.9f));
        DrawText("2D Cizim ve Sekiller", 15, 10, 24, WHITE);

        DrawText("Dikdortgenler:", 20, 58, 15, DARKGRAY);
        DrawRectangle(20, 80, 80, 50, RED);
        DrawRectangleLines(120, 80, 80, 50, BLUE);
        DrawRectangleRounded((Rectangle){220, 80, 80, 50}, 0.3f, 4, GREEN);
        DrawRectangleGradientH(320, 80, 80, 50, SKYBLUE, DARKPURPLE);

        DrawText("Daireler:", 20, 165, 15, DARKGRAY);
        DrawCircle(60, 220, 30, MAROON);
        DrawCircleLines(160, 220, 30, DARKBLUE);
        DrawCircleSector((Vector2){260, 220}, 30, 0, 120 + sinf(t)*60, 16, ORANGE);
        DrawRing((Vector2){360, 220}, 15, 30, 0, 270, 16, PURPLE);

        DrawText("Cizgiler:", 20, 285, 15, DARKGRAY);
        DrawLine(20, 315, 120, 350, RED);
        DrawLineEx((Vector2){140, 315}, (Vector2){240, 350}, 3.0f, BLUE);
        DrawLineBezier((Vector2){260, 340}, (Vector2){400, 310}, 2.0f, DARKGREEN);

        DrawText("Ucgen & Poligon:", 20, 388, 15, DARKGRAY);
        DrawTriangle((Vector2){60, 420}, (Vector2){20, 480}, (Vector2){100, 480}, GOLD);
        DrawPoly((Vector2){180, 450}, 6, 35, t * 30, VIOLET);

        DrawText("Yazi:", 450, 58, 15, DARKGRAY);
        DrawText("DrawText - varsayilan font", 450, 80, 18, DARKGRAY);
        DrawText(TextFormat("Frame: %d  FPS: %d", frame, GetFPS()), 450, 105, 14, MAROON);
        int olcum = MeasureText("Merkezlenmis Yazi", 20);
        DrawText("Merkezlenmis Yazi", (W - olcum) / 2, 160, 20, DARKBLUE);

        DrawText("Doku:", 450, 195, 15, DARKGRAY);
        DrawTexture(doku, 450, 215, WHITE);
        DrawTextureEx(doku, (Vector2){550, 215}, sinf(t) * 15.0f, 1.5f, SKYBLUE);

        DrawText("Carpisma:", 450, 340, 15, DARKGRAY);
        Color kutuRenk = carpisiyor ? RED : Fade(SKYBLUE, 0.5f);
        DrawRectangleRec(sabitKutu, kutuRenk);
        Color daireRenk = carpisiyor ? RED : GREEN;
        DrawCircleV(dairePos, daireR, Fade(daireRenk, 0.6f));
        if (carpisiyor) DrawText("CARPISMA!", 620, 555, 20, RED);
        EndDrawing();
    }

    UnloadTexture(doku);
    CloseWindow();
    return 0;
}
