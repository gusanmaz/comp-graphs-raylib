#include "raylib.h"
#include <math.h>
#include <float.h>

/*
 * Ornek 06 - Specular (Aynamsı) Aydinlatma ile Isin Izleyici
 *
 * Diffuse modele specular yansima eklenir.
 * Her kurenin bir "specular" ustu (parlaklık katsayisi) vardir.
 * R = 2N(N·L) - L formuluyle yansima vektoru hesaplanir.
 * cos(alpha)^s ile parlak noktalar olusturulur.
 */

// ---- Vektor Islemleri ----
typedef struct { float x, y, z; } Vec3;

Vec3 v_add(Vec3 a, Vec3 b) { return (Vec3){a.x+b.x, a.y+b.y, a.z+b.z}; }
Vec3 v_sub(Vec3 a, Vec3 b) { return (Vec3){a.x-b.x, a.y-b.y, a.z-b.z}; }
Vec3 v_scl(Vec3 v, float s) { return (Vec3){v.x*s, v.y*s, v.z*s}; }
float v_dot(Vec3 a, Vec3 b) { return a.x*b.x + a.y*b.y + a.z*b.z; }
float v_len(Vec3 v) { return sqrtf(v_dot(v, v)); }
Vec3 v_norm(Vec3 v) { float l = v_len(v); return (Vec3){v.x/l, v.y/l, v.z/l}; }

// ---- Kure (specular eklendi) ----
typedef struct {
    Vec3 center;
    float radius;
    unsigned char r, g, b;
    int specular;  // -1 = mat, >0 = parlak
} Sphere;

#define SPHERE_COUNT 4
Sphere spheres[SPHERE_COUNT] = {
    {{ 0.0f, -1.0f,  3.0f}, 1.0f,    255,   0,   0,  500},  // Kirmizi - parlak
    {{ 2.0f,  0.0f,  4.0f}, 1.0f,      0,   0, 255,  500},  // Mavi    - parlak
    {{-2.0f,  0.0f,  4.0f}, 1.0f,      0, 255,   0,   10},  // Yesil   - biraz parlak
    {{ 0.0f,-5001.0f,0.0f}, 5000.0f, 255, 255,   0, 1000},  // Zemin   - cok parlak
};

// ---- Isik Kaynaklari ----
typedef enum { L_AMBIENT, L_POINT, L_DIRECTIONAL } LType;
typedef struct { LType type; float intensity; Vec3 pos; Vec3 dir; } Light;

#define LIGHT_COUNT 3
Light lights[LIGHT_COUNT] = {
    { L_AMBIENT,     0.2f, {0,0,0}, {0,0,0}  },
    { L_POINT,       0.6f, {2,1,0}, {0,0,0}  },
    { L_DIRECTIONAL, 0.2f, {0,0,0}, {1,4,4}  },
};

// ---- Isin-Kure Kesisimi ----
void IntersectRS(Vec3 O, Vec3 D, Sphere s, float *t1, float *t2)
{
    Vec3 CO = v_sub(O, s.center);
    float a = v_dot(D, D);
    float b = 2.0f * v_dot(CO, D);
    float c = v_dot(CO, CO) - s.radius * s.radius;
    float disc = b*b - 4*a*c;
    if (disc < 0) { *t1 = FLT_MAX; *t2 = FLT_MAX; return; }
    float sq = sqrtf(disc);
    *t1 = (-b + sq) / (2*a);
    *t2 = (-b - sq) / (2*a);
}

// ---- Aydinlatma: Diffuse + Specular ----
float ComputeLighting(Vec3 P, Vec3 N, Vec3 V, int spec)
{
    float i = 0.0f;
    for (int li = 0; li < LIGHT_COUNT; li++) {
        if (lights[li].type == L_AMBIENT) {
            i += lights[li].intensity;
            continue;
        }

        Vec3 L = (lights[li].type == L_POINT)
                 ? v_sub(lights[li].pos, P)
                 : lights[li].dir;

        // Diffuse
        float ndl = v_dot(N, L);
        if (ndl > 0)
            i += lights[li].intensity * ndl / (v_len(N) * v_len(L));

        // Specular
        if (spec != -1) {
            // R = 2N(N·L) - L
            Vec3 R = v_sub(v_scl(N, 2.0f * v_dot(N, L)), L);
            float rdv = v_dot(R, V);
            if (rdv > 0) {
                float factor = powf(rdv / (v_len(R) * v_len(V)), (float)spec);
                i += lights[li].intensity * factor;
            }
        }
    }
    return i;
}

// ---- Isin Izleme ----
Color TraceRay(Vec3 O, Vec3 D, float t_min, float t_max)
{
    float closest_t = FLT_MAX;
    int idx = -1;

    for (int i = 0; i < SPHERE_COUNT; i++) {
        float t1, t2;
        IntersectRS(O, D, spheres[i], &t1, &t2);
        if (t1 >= t_min && t1 <= t_max && t1 < closest_t) { closest_t = t1; idx = i; }
        if (t2 >= t_min && t2 <= t_max && t2 < closest_t) { closest_t = t2; idx = i; }
    }

    if (idx == -1) return RAYWHITE;

    Vec3 P = v_add(O, v_scl(D, closest_t));
    Vec3 N = v_norm(v_sub(P, spheres[idx].center));
    Vec3 V = v_scl(D, -1.0f);  // V = -D

    float light = ComputeLighting(P, N, V, spheres[idx].specular);
    if (light > 1.0f) light = 1.0f;

    unsigned char cr = (unsigned char)fminf(255, spheres[idx].r * light);
    unsigned char cg = (unsigned char)fminf(255, spheres[idx].g * light);
    unsigned char cb = (unsigned char)fminf(255, spheres[idx].b * light);
    return (Color){cr, cg, cb, 255};
}

Vec3 CanvasToViewport(int cx, int cy, int cw, int ch)
{
    return (Vec3){ (float)cx/(float)cw, (float)cy/(float)ch, 1.0f };
}

int main(void)
{
    const int CW = 600, CH = 600;
    InitWindow(CW, CH, "Ornek 06 - Specular Aydinlatma Raytracer");

    Image img = GenImageColor(CW, CH, RAYWHITE);
    Vec3 O = {0, 0, 0};

    for (int x = -CW/2; x < CW/2; x++) {
        for (int y = -CH/2; y < CH/2; y++) {
            Vec3 D = CanvasToViewport(x, y, CW, CH);
            Color c = TraceRay(O, D, 1.0f, FLT_MAX);
            int sx = x + CW/2;
            int sy = CH/2 - y;
            if (sx >= 0 && sx < CW && sy >= 0 && sy < CH)
                ImageDrawPixel(&img, sx, sy, c);
        }
    }

    Texture2D tex = LoadTextureFromImage(img);
    UnloadImage(img);
    SetTargetFPS(60);

    while (!WindowShouldClose()) {
        BeginDrawing();
            ClearBackground(RAYWHITE);
            DrawTexture(tex, 0, 0, WHITE);
            DrawRectangle(0, 0, CW, 55, Fade(BLACK, 0.6f));
            DrawText("Diffuse + Specular Aydinlatma", 10, 8, 22, WHITE);
            DrawText("Kirmizi(s=500) Mavi(s=500) Yesil(s=10) Zemin(s=1000)",
                     10, 33, 14, LIGHTGRAY);
        EndDrawing();
    }

    UnloadTexture(tex);
    CloseWindow();
    return 0;
}
