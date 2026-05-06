#include "raylib.h"
#include <math.h>

/*
 * Ornek 07 - C Temelleri ve Raylib Veri Tipleri
 *
 * C dilinin temel yapilarini ve raylib veri tiplerini gorsellestir.
 * Derleme: cc -o ornek07 ornek07_c_temelleri.c -lraylib -lm
 */

typedef struct {
    float x;
    float y;
    float yaricap;
    Color renk;
} Daire;

int main(void)
{
    int sayac = 0;
    float hiz = 2.5f;
    bool aktif = true;

    Vector2 konum2d = { 400.0f, 300.0f };
    Vector3 konum3d = { 1.0f, 2.0f, 3.0f };
    Color   renk    = { 255, 100, 50, 255 };
    Rectangle kutu  = { 50, 400, 200, 80 };

    Daire daire1 = { 600.0f, 250.0f, 40.0f, BLUE };
    Daire daire2 = { 300.0f, 450.0f, 25.0f, GREEN };

    InitWindow(900, 600, "Ornek 07 - C Temelleri ve Raylib Veri Tipleri");
    SetTargetFPS(60);

    while (!WindowShouldClose())
    {
        sayac++;
        Vector2 fare = GetMousePosition();
        konum2d.x += (fare.x - konum2d.x) * 0.02f;
        konum2d.y += (fare.y - konum2d.y) * 0.02f;
        renk.g = (unsigned char)(128 + 127 * sinf(sayac * 0.03f));
        renk.b = (unsigned char)(128 + 127 * cosf(sayac * 0.03f));
        daire1.x = 600.0f + sinf(sayac * 0.05f) * 100.0f;

        BeginDrawing();
            ClearBackground(RAYWHITE);
            DrawText("C Temelleri ve Raylib Veri Tipleri", 20, 15, 24, DARKGRAY);

            DrawText(TextFormat("int   sayac = %d", sayac), 20, 60, 18, DARKBLUE);
            DrawText(TextFormat("float hiz   = %.1f", hiz), 20, 85, 18, DARKBLUE);
            DrawText(TextFormat("bool  aktif = %s", aktif ? "true" : "false"), 20, 110, 18, DARKBLUE);

            DrawCircleV(konum2d, 12.0f, RED);
            DrawText(TextFormat("Vector2 konum2d = { %.0f, %.0f }", konum2d.x, konum2d.y), 20, 145, 16, MAROON);

            DrawText(TextFormat("Vector3 konum3d = { %.1f, %.1f, %.1f }", konum3d.x, konum3d.y, konum3d.z), 20, 195, 16, DARKGREEN);

            DrawRectangle(20, 245, 60, 30, renk);
            DrawRectangleLines(20, 245, 60, 30, DARKGRAY);
            DrawText(TextFormat("Color renk = { %d, %d, %d, %d }", renk.r, renk.g, renk.b, renk.a), 90, 250, 16, DARKGRAY);

            DrawRectangle(20, 310, 25, 25, RED);
            DrawRectangle(50, 310, 25, 25, GREEN);
            DrawRectangle(80, 310, 25, 25, BLUE);
            DrawRectangle(110, 310, 25, 25, YELLOW);
            DrawRectangle(140, 310, 25, 25, PURPLE);
            DrawText("Hazir renkler: RED, GREEN, BLUE, YELLOW, PURPLE ...", 175, 315, 14, GRAY);

            DrawRectangleRec(kutu, Fade(SKYBLUE, 0.5f));
            DrawRectangleLinesEx(kutu, 2, DARKBLUE);
            DrawText(TextFormat("Rectangle kutu = { %.0f, %.0f, %.0f, %.0f }", kutu.x, kutu.y, kutu.width, kutu.height), 20, 385, 16, DARKBLUE);

            DrawCircle((int)daire1.x, (int)daire1.y, daire1.yaricap, daire1.renk);
            DrawCircle((int)daire2.x, (int)daire2.y, daire2.yaricap, daire2.renk);
            DrawText("Kendi struct: Daire { x, y, yaricap, renk }", 20, 530, 16, DARKPURPLE);
            DrawText(TextFormat("daire1.x = %.0f  (sag-sol sallanir)", daire1.x), 20, 555, 13, GRAY);
        EndDrawing();
    }

    CloseWindow();
    return 0;
}
