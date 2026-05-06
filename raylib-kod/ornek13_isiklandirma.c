#include "raylib.h"
#include "raymath.h"

/*
 * Ornek 13 - Isiklandirma Temelleri (Lambert diffuse + ambient)
 * WASD: isik tasi, UP/DOWN: isik Y, SPACE: ambient, 1/2/3: isik rengi
 * Derleme: cc -o ornek13 ornek13_isiklandirma.c -lraylib -lm
 */

float lambert(Vector3 N, Vector3 L)
{
    float d = Vector3DotProduct(N, L);
    return d > 0.0f ? d : 0.0f;
}

Color skalaRenk(Color c, float k)
{
    if (k > 1.0f) k = 1.0f;
    return (Color){ (unsigned char)(c.r*k), (unsigned char)(c.g*k), (unsigned char)(c.b*k), 255 };
}

int main(void)
{
    const int W = 950, H = 650;
    InitWindow(W, H, "Ornek 13 - Isiklandirma");
    SetTargetFPS(60);

    Camera3D kam = { {6,6,6}, {0,0,0}, {0,1,0}, 50, CAMERA_PERSPECTIVE };
    Vector3 isikPos = { 3, 4, 2 };
    Color isikRenk = WHITE;
    float ambient = 0.1f;
    bool ambOn = true;

    Vector3 kutuN[6] = { {0,0,-1},{0,0,1},{-1,0,0},{1,0,0},{0,1,0},{0,-1,0} };

    while (!WindowShouldClose())
    {
        UpdateCamera(&kam, CAMERA_ORBITAL);
        float h = 0.1f;
        if (IsKeyDown(KEY_D)) isikPos.x += h;
        if (IsKeyDown(KEY_A)) isikPos.x -= h;
        if (IsKeyDown(KEY_W)) isikPos.z -= h;
        if (IsKeyDown(KEY_S)) isikPos.z += h;
        if (IsKeyDown(KEY_UP))   isikPos.y += h;
        if (IsKeyDown(KEY_DOWN)) isikPos.y -= h;
        if (IsKeyPressed(KEY_SPACE)) ambOn = !ambOn;
        ambient = ambOn ? 0.1f : 0.0f;
        if (IsKeyPressed(KEY_ONE))   isikRenk = WHITE;
        if (IsKeyPressed(KEY_TWO))   isikRenk = YELLOW;
        if (IsKeyPressed(KEY_THREE)) isikRenk = SKYBLUE;

        Vector3 kutuM = { 0, 0.75f, 0 };
        Vector3 Lk = Vector3Normalize(Vector3Subtract(isikPos, kutuM));
        Vector3 kureM = { -2.5f, 0.75f, 0 };
        Vector3 Ls = Vector3Normalize(Vector3Subtract(isikPos, kureM));
        Vector3 silM = { 2.5f, 0.75f, 0 };
        Vector3 Lc = Vector3Normalize(Vector3Subtract(isikPos, silM));

        BeginDrawing();
            ClearBackground((Color){30,30,40,255});
            BeginMode3D(kam);
                DrawGrid(10, 1.0f);
                DrawSphere(isikPos, 0.15f, isikRenk);
                DrawLine3D(isikPos, kutuM, Fade(YELLOW, 0.3f));
                DrawLine3D(isikPos, kureM, Fade(YELLOW, 0.3f));

                float b = 1.5f, y = b/2;
                for (int i = 0; i < 6; i++) {
                    float lam = lambert(kutuN[i], Lk);
                    Color c = skalaRenk(RED, ambient + lam * 0.9f);
                    Vector3 p = Vector3Add(kutuM, Vector3Scale(kutuN[i], y));
                    DrawCube(p,
                        kutuN[i].x!=0 ? 0.02f : b-0.01f,
                        kutuN[i].y!=0 ? 0.02f : b-0.01f,
                        kutuN[i].z!=0 ? 0.02f : b-0.01f, c);
                }
                DrawCubeWires(kutuM, b,b,b, Fade(WHITE, 0.3f));

                float kl = lambert(Ls, (Vector3){0,1,0});
                DrawSphere(kureM, 0.75f, skalaRenk(BLUE, ambient + kl*0.9f));
                DrawSphereWires(kureM, 0.75f, 12, 12, Fade(WHITE, 0.15f));

                float sl = lambert(Lc, (Vector3){0,1,0});
                DrawCylinder(silM, 0.5f,0.5f,1.5f,16, skalaRenk(GREEN, ambient + sl*0.9f));

                float zl = lambert((Vector3){0,1,0}, Vector3Normalize(Vector3Subtract(isikPos, (Vector3){0,0,0})));
                DrawPlane((Vector3){0,0,0}, (Vector2){10,10}, skalaRenk((Color){80,80,80,255}, ambient + zl*0.8f));

                for (int i = 0; i < 6; i++) {
                    Vector3 s = Vector3Add(kutuM, Vector3Scale(kutuN[i], y));
                    DrawLine3D(s, Vector3Add(s, Vector3Scale(kutuN[i], 0.5f)), YELLOW);
                }
            EndMode3D();

            DrawRectangle(0,0,W,50, Fade(BLACK, 0.8f));
            DrawText("Isiklandirma Temelleri", 15, 13, 22, WHITE);
            DrawRectangle(5,55,300,110, Fade(WHITE, 0.85f));
            DrawText("WASD:isik XZ  UP/DOWN:Y", 15, 62, 12, GRAY);
            DrawText(TextFormat("SPACE: ambient %s", ambOn?"ON":"OFF"), 15, 80, 12, GRAY);
            DrawText("[1]Beyaz [2]Sari [3]Mavi", 15, 98, 12, GRAY);
            DrawText("renk = base*(ambient+lambert)", 15, 120, 12, DARKGREEN);
            DrawText("lambert = max(0, dot(N, L))", 15, 138, 12, DARKGREEN);
        EndDrawing();
    }
    CloseWindow();
    return 0;
}
