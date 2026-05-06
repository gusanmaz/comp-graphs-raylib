#include "raylib.h"

/*
 * Ornek 08 - Girdi Isleme (Klavye, Fare, Gamepad)
 * Derleme: cc -o ornek08 ornek08_girdi_isleme.c -lraylib -lm
 */

int main(void)
{
    const int W = 900, H = 650;
    InitWindow(W, H, "Ornek 08 - Girdi Isleme");
    SetTargetFPS(60);

    Vector2 kutuPos = { 400.0f, 300.0f };
    float kutuBoyut = 40.0f;
    Color kutuRenk = BLUE;
    float kutuHiz = 4.0f;

    Vector2 noktalar[1024];
    int noktaSayisi = 0;
    float zoom = 1.0f;
    char sonTus[64] = "Henuz tus basilmadi";
    int basilmaSayisi = 0;

    while (!WindowShouldClose())
    {
        if (IsKeyDown(KEY_RIGHT) || IsKeyDown(KEY_D)) kutuPos.x += kutuHiz;
        if (IsKeyDown(KEY_LEFT)  || IsKeyDown(KEY_A)) kutuPos.x -= kutuHiz;
        if (IsKeyDown(KEY_DOWN)  || IsKeyDown(KEY_S)) kutuPos.y += kutuHiz;
        if (IsKeyDown(KEY_UP)    || IsKeyDown(KEY_W)) kutuPos.y -= kutuHiz;

        if (IsKeyPressed(KEY_SPACE)) {
            kutuRenk = (Color){ GetRandomValue(50,255), GetRandomValue(50,255), GetRandomValue(50,255), 255 };
            basilmaSayisi++;
            TextCopy(sonTus, "SPACE");
        }
        if (IsKeyPressed(KEY_R)) {
            kutuPos = (Vector2){ 400.0f, 300.0f };
            kutuRenk = BLUE;
            noktaSayisi = 0;
            TextCopy(sonTus, "R (sifirlandi)");
        }
        if (kutuPos.x < 0) kutuPos.x = 0;
        if (kutuPos.y < 0) kutuPos.y = 0;
        if (kutuPos.x > W - kutuBoyut) kutuPos.x = W - kutuBoyut;
        if (kutuPos.y > H - kutuBoyut) kutuPos.y = H - kutuBoyut;

        Vector2 farePos = GetMousePosition();
        if (IsMouseButtonDown(MOUSE_BUTTON_LEFT) && noktaSayisi < 1024) {
            noktalar[noktaSayisi] = farePos;
            noktaSayisi++;
        }
        if (IsMouseButtonPressed(MOUSE_BUTTON_RIGHT) && noktaSayisi > 0) noktaSayisi--;

        float tekerlek = GetMouseWheelMove();
        if (tekerlek != 0) {
            zoom += tekerlek * 0.1f;
            if (zoom < 0.2f) zoom = 0.2f;
            if (zoom > 3.0f) zoom = 3.0f;
        }

        BeginDrawing();
            ClearBackground(RAYWHITE);
            DrawRectangle(0, 0, W, 50, Fade(DARKBLUE, 0.9f));
            DrawText("Girdi Isleme: Klavye, Fare, Tekerlek", 15, 13, 22, WHITE);

            DrawRectangle(5, 58, 280, 200, Fade(LIGHTGRAY, 0.3f));
            DrawText("KLAVYE:", 15, 65, 16, DARKBLUE);
            DrawText("WASD / Oklar : kutuyu tasi", 15, 88, 13, GRAY);
            DrawText("SPACE : renk degistir", 15, 106, 13, GRAY);
            DrawText("R : sifirla", 15, 124, 13, GRAY);
            DrawText(TextFormat("Son tus: %s", sonTus), 15, 152, 14, MAROON);
            DrawText(TextFormat("SPACE sayaci: %d", basilmaSayisi), 15, 172, 14, DARKGREEN);

            DrawRectangle(615, 58, 275, 200, Fade(LIGHTGRAY, 0.3f));
            DrawText("FARE:", 625, 65, 16, DARKBLUE);
            DrawText(TextFormat("Konum: (%.0f, %.0f)", farePos.x, farePos.y), 625, 88, 13, GRAY);
            DrawText("Sol buton: ciz (basili tut)", 625, 106, 13, GRAY);
            DrawText("Sag buton: son noktayi sil", 625, 124, 13, GRAY);
            DrawText(TextFormat("Zoom: %.1fx", zoom), 625, 170, 14, DARKGREEN);

            DrawCircle(640, 248, 8, IsMouseButtonDown(MOUSE_BUTTON_LEFT) ? GREEN : LIGHTGRAY);
            DrawText("Sol", 655, 241, 13, GRAY);
            DrawCircle(700, 248, 8, IsMouseButtonDown(MOUSE_BUTTON_MIDDLE) ? GREEN : LIGHTGRAY);
            DrawText("Orta", 715, 241, 13, GRAY);
            DrawCircle(766, 248, 8, IsMouseButtonDown(MOUSE_BUTTON_RIGHT) ? GREEN : LIGHTGRAY);
            DrawText("Sag", 781, 241, 13, GRAY);

            float boyut = kutuBoyut * zoom;
            DrawRectangle((int)kutuPos.x, (int)kutuPos.y, (int)boyut, (int)boyut, kutuRenk);
            DrawRectangleLines((int)kutuPos.x, (int)kutuPos.y, (int)boyut, (int)boyut, BLACK);

            for (int i = 0; i < noktaSayisi; i++) {
                DrawCircleV(noktalar[i], 3.0f, RED);
                if (i > 0) DrawLineV(noktalar[i-1], noktalar[i], Fade(RED, 0.4f));
            }
            DrawCircleLines((int)farePos.x, (int)farePos.y, 15, Fade(DARKGRAY, 0.5f));
        EndDrawing();
    }

    CloseWindow();
    return 0;
}
