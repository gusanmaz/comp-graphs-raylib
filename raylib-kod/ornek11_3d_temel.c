#include "raylib.h"
#include <math.h>

/*
 * Ornek 11 - 3D Temel Kavramlar ve Projeksiyon
 * Sol: perspektif, Sag: ortografik
 * Derleme: cc -o ornek11 ornek11_3d_temel.c -lraylib -lm
 */

int main(void)
{
    const int W = 1000, H = 600;
    InitWindow(W, H, "Ornek 11 - 3D Temel ve Projeksiyon");
    SetTargetFPS(60);

    Camera3D kamP = { {6,6,6}, {0,0.5f,0}, {0,1,0}, 50, CAMERA_PERSPECTIVE };
    Camera3D kamO = { {6,6,6}, {0,0.5f,0}, {0,1,0}, 12, CAMERA_ORTHOGRAPHIC };

    float donme = 0.0f;
    bool otoDon = true;

    while (!WindowShouldClose())
    {
        if (IsKeyPressed(KEY_SPACE)) otoDon = !otoDon;
        if (otoDon) donme += 0.5f;
        if (IsKeyDown(KEY_UP))   kamP.fovy -= 0.5f;
        if (IsKeyDown(KEY_DOWN)) kamP.fovy += 0.5f;
        if (kamP.fovy < 10) kamP.fovy = 10;
        if (kamP.fovy > 120) kamP.fovy = 120;

        float rad = donme * DEG2RAD;
        kamP.position = (Vector3){ cosf(rad)*8, 5, sinf(rad)*8 };
        kamO.position = kamP.position;

        BeginDrawing();
            ClearBackground(RAYWHITE);

            BeginScissorMode(0, 0, W/2, H);
            BeginMode3D(kamP);
                DrawGrid(10, 1.0f);
                DrawLine3D((Vector3){0,0,0}, (Vector3){3,0,0}, RED);
                DrawLine3D((Vector3){0,0,0}, (Vector3){0,3,0}, GREEN);
                DrawLine3D((Vector3){0,0,0}, (Vector3){0,0,3}, BLUE);
                DrawCube((Vector3){0,0.5f,0}, 1,1,1, Fade(RED, 0.7f));
                DrawCubeWires((Vector3){0,0.5f,0}, 1,1,1, MAROON);
                DrawSphere((Vector3){2,0.5f,0}, 0.5f, Fade(BLUE, 0.7f));
                DrawCylinder((Vector3){-2,0,0}, 0.5f,0.5f,1.5f,12, Fade(GREEN, 0.7f));
                DrawCube((Vector3){0,0.4f,2.5f}, 2,0.8f,0.8f, Fade(ORANGE, 0.7f));
            EndMode3D();
            EndScissorMode();

            BeginScissorMode(W/2, 0, W/2, H);
            ClearBackground((Color){245,245,250,255});
            BeginMode3D(kamO);
                DrawGrid(10, 1.0f);
                DrawLine3D((Vector3){0,0,0}, (Vector3){3,0,0}, RED);
                DrawLine3D((Vector3){0,0,0}, (Vector3){0,3,0}, GREEN);
                DrawLine3D((Vector3){0,0,0}, (Vector3){0,0,3}, BLUE);
                DrawCube((Vector3){0,0.5f,0}, 1,1,1, Fade(RED, 0.7f));
                DrawSphere((Vector3){2,0.5f,0}, 0.5f, Fade(BLUE, 0.7f));
                DrawCylinder((Vector3){-2,0,0}, 0.5f,0.5f,1.5f,12, Fade(GREEN, 0.7f));
                DrawCube((Vector3){0,0.4f,2.5f}, 2,0.8f,0.8f, Fade(ORANGE, 0.7f));
            EndMode3D();
            EndScissorMode();

            DrawLine(W/2, 0, W/2, H, DARKGRAY);
            DrawRectangle(10, 10, 200, 28, Fade(BLACK, 0.6f));
            DrawText("PERSPEKTIF", 20, 15, 18, WHITE);
            DrawRectangle(W/2+10, 10, 200, 28, Fade(BLACK, 0.6f));
            DrawText("ORTOGRAFIK", W/2+20, 15, 18, WHITE);

            DrawText(TextFormat("SPACE:don  UP/DOWN:fov(%.0f)", kamP.fovy), 10, H-25, 13, GRAY);
        EndDrawing();
    }
    CloseWindow();
    return 0;
}
