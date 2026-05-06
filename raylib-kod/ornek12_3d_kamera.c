#include "raylib.h"

/*
 * Ornek 12 - 3D Kamera Modlari
 * 1-4 tuslari ile mod degistir
 * Derleme: cc -o ornek12 ornek12_3d_kamera.c -lraylib -lm
 */

int main(void)
{
    const int W = 950, H = 600;
    InitWindow(W, H, "Ornek 12 - 3D Kamera Modlari");

    Camera3D kam = { {5,5,5}, {0,0,0}, {0,1,0}, 55, CAMERA_PERSPECTIVE };
    int mi = 0;
    int modlar[] = { CAMERA_FREE, CAMERA_ORBITAL, CAMERA_FIRST_PERSON, CAMERA_THIRD_PERSON };
    const char *ad[] = { "FREE", "ORBITAL", "FIRST_PERSON", "THIRD_PERSON" };

    Vector3 kp[] = { {0,0.5f,0},{3,0.5f,0},{-3,0.5f,0},{0,0.5f,3},{0,0.5f,-3},{3,1,3},{-3,0.5f,-3} };
    Color kr[] = { RED, BLUE, GREEN, ORANGE, PURPLE, GOLD, SKYBLUE };

    DisableCursor();
    SetTargetFPS(60);

    while (!WindowShouldClose())
    {
        if (IsKeyPressed(KEY_ONE))   { mi=0; kam.position=(Vector3){5,5,5}; }
        if (IsKeyPressed(KEY_TWO))   { mi=1; kam.position=(Vector3){5,5,5}; }
        if (IsKeyPressed(KEY_THREE)) { mi=2; kam.position=(Vector3){0,2,0}; kam.target=(Vector3){0,2,1}; }
        if (IsKeyPressed(KEY_FOUR))  { mi=3; kam.position=(Vector3){0,2,-5}; kam.target=(Vector3){0,0,0}; }
        if (IsKeyPressed(KEY_M)) { if (IsCursorHidden()) EnableCursor(); else DisableCursor(); }

        UpdateCamera(&kam, modlar[mi]);

        BeginDrawing();
            ClearBackground((Color){180,200,220,255});
            BeginMode3D(kam);
                DrawPlane((Vector3){0,0,0}, (Vector2){30,30}, Fade(DARKGREEN, 0.6f));
                DrawGrid(30, 1.0f);
                DrawLine3D((Vector3){0,0,0}, (Vector3){5,0,0}, RED);
                DrawLine3D((Vector3){0,0,0}, (Vector3){0,5,0}, GREEN);
                DrawLine3D((Vector3){0,0,0}, (Vector3){0,0,5}, BLUE);
                for (int i = 0; i < 7; i++) {
                    DrawCube(kp[i], 0.8f,0.8f,0.8f, Fade(kr[i], 0.7f));
                    DrawCubeWires(kp[i], 0.8f,0.8f,0.8f, kr[i]);
                }
                DrawCylinder((Vector3){-2,0,2}, 0.3f,0.3f,2, 12, BROWN);
                DrawSphere((Vector3){-2,2.3f,2}, 0.4f, YELLOW);
            EndMode3D();

            DrawRectangle(0,0,W,50, Fade(BLACK, 0.7f));
            DrawText("3D Kamera Modlari", 15, 13, 22, WHITE);
            DrawText(TextFormat("Mod: %s", ad[mi]), 300, 16, 16, YELLOW);

            DrawRectangle(5,55,310,145, Fade(WHITE, 0.85f));
            DrawText("[1] FREE   [2] ORBITAL", 15, 62, 12, mi<2 ? RED : GRAY);
            DrawText("[3] FIRST  [4] THIRD", 15, 80, 12, mi>=2 ? RED : GRAY);
            DrawText("[M] fare goster/gizle", 15, 104, 12, DARKGREEN);
            DrawText(TextFormat("pos=(%.1f,%.1f,%.1f)", kam.position.x, kam.position.y, kam.position.z), 15, 130, 12, GRAY);
            DrawText(TextFormat("tgt=(%.1f,%.1f,%.1f)", kam.target.x, kam.target.y, kam.target.z), 15, 148, 12, GRAY);
            DrawText(TextFormat("fov=%.1f", kam.fovy), 15, 166, 12, GRAY);
        EndDrawing();
    }
    CloseWindow();
    return 0;
}
