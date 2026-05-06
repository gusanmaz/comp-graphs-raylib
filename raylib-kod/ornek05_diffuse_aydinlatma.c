#include "raylib.h"
#include <math.h>
#include <float.h>

/*
 * Ornek 05 - Diffuse (Yayinik) Aydinlatma ile Isin Izleyici
 *
 * Onceki basit raytracer'a diffuse aydinlatma modeli ekler.
 * Isik kaynaklari: 1 ambient, 1 noktasal, 1 yonlu
 * Her pikselde yuzeyin normali hesaplanir ve isik
 * yogunlugu dot(N, L) ile belirlenir.
 */

// ---- Vektor Islemleri ----
typedef struct { float x, y, z; } Vec3;

Vec3 vec3_add(Vec3 a, Vec3 b) { return (Vec3){a.x+b.x, a.y+b.y, a.z+b.z}; }
Vec3 vec3_sub(Vec3 a, Vec3 b) { return (Vec3){a.x-b.x, a.y-b.y, a.z-b.z}; }
Vec3 vec3_scale(Vec3 v, float s) { return (Vec3){v.x*s, v.y*s, v.z*s}; }
float vec3_dot(Vec3 a, Vec3 b) { return a.x*b.x + a.y*b.y + a.z*b.z; }
float vec3_len(Vec3 v) { return sqrtf(vec3_dot(v, v)); }
Vec3 vec3_norm(Vec3 v) { float l = vec3_len(v); return (Vec3){v.x/l, v.y/l, v.z/l}; }

// ---- Kure ----
typedef struct {
    Vec3 center;
    float radius;
    unsigned char r, g, b;
} Sphere;

#define SPHERE_COUNT 4
Sphere spheres[SPHERE_COUNT] = {
    {{ 0.0f, -1.0f,  3.0f}, 1.0f,    255,   0,   0},   // Kirmizi
    {{ 2.0f,  0.0f,  4.0f}, 1.0f,      0,   0, 255},   // Mavi
    {{-2.0f,  0.0f,  4.0f}, 1.0f,      0, 255,   0},   // Yesil
    {{ 0.0f,-5001.0f,0.0f}, 5000.0f, 255, 255,   0},   // Sari zemin
};

// ---- Isik Kaynaklari ----
typedef enum { LIGHT_AMBIENT, LIGHT_POINT, LIGHT_DIRECTIONAL } LightType;

typedef struct {
    LightType type;
    float intensity;
    Vec3 position;   // noktasal icin
    Vec3 direction;  // yonlu icin
} Light;

#define LIGHT_COUNT 3
Light lights[LIGHT_COUNT] = {
    { LIGHT_AMBIENT,     0.2f, {0,0,0},   {0,0,0}     },
    { LIGHT_POINT,       0.6f, {2,1,0},   {0,0,0}     },
    { LIGHT_DIRECTIONAL, 0.2f, {0,0,0},   {1,4,4}     },
};

// ---- Isin-Kure Kesisimi ----
void IntersectRaySphere(Vec3 O, Vec3 D, Sphere s, float *t1, float *t2)
{
    Vec3 CO = vec3_sub(O, s.center);
    float a = vec3_dot(D, D);
    float b = 2.0f * vec3_dot(CO, D);
    float c = vec3_dot(CO, CO) - s.radius * s.radius;
    float disc = b*b - 4*a*c;
    if (disc < 0) { *t1 = FLT_MAX; *t2 = FLT_MAX; return; }
    float sq = sqrtf(disc);
    *t1 = (-b + sq) / (2*a);
    *t2 = (-b - sq) / (2*a);
}

// ---- Diffuse Aydinlatma Hesabi ----
float ComputeLighting(Vec3 P, Vec3 N)
{
    float intensity = 0.0f;
    for (int i = 0; i < LIGHT_COUNT; i++) {
        if (lights[i].type == LIGHT_AMBIENT) {
            intensity += lights[i].intensity;
        } else {
            Vec3 L;
            if (lights[i].type == LIGHT_POINT)
                L = vec3_sub(lights[i].position, P);
            else
                L = lights[i].direction;

            float n_dot_l = vec3_dot(N, L);
            if (n_dot_l > 0) {
                intensity += lights[i].intensity * n_dot_l / (vec3_len(N) * vec3_len(L));
            }
        }
    }
    return intensity;
}

// ---- Isin Izleme ----
Color TraceRay(Vec3 O, Vec3 D, float t_min, float t_max)
{
    float closest_t = FLT_MAX;
    int closest_idx = -1;

    for (int i = 0; i < SPHERE_COUNT; i++) {
        float t1, t2;
        IntersectRaySphere(O, D, spheres[i], &t1, &t2);
        if (t1 >= t_min && t1 <= t_max && t1 < closest_t) { closest_t = t1; closest_idx = i; }
        if (t2 >= t_min && t2 <= t_max && t2 < closest_t) { closest_t = t2; closest_idx = i; }
    }

    if (closest_idx == -1) return RAYWHITE;

    // Kesisim noktasi ve normal
    Vec3 P = vec3_add(O, vec3_scale(D, closest_t));
    Vec3 N = vec3_sub(P, spheres[closest_idx].center);
    N = vec3_norm(N);

    // Aydinlatma
    float light = ComputeLighting(P, N);
    if (light > 1.0f) light = 1.0f;

    unsigned char cr = (unsigned char)(spheres[closest_idx].r * light);
    unsigned char cg = (unsigned char)(spheres[closest_idx].g * light);
    unsigned char cb = (unsigned char)(spheres[closest_idx].b * light);
    return (Color){cr, cg, cb, 255};
}

// ---- Canvas -> Viewport ----
Vec3 CanvasToViewport(int cx, int cy, int cw, int ch)
{
    return (Vec3){ (float)cx/(float)cw, (float)cy/(float)ch, 1.0f };
}

int main(void)
{
    const int CW = 600, CH = 600;
    InitWindow(CW, CH, "Ornek 05 - Diffuse Aydinlatma Raytracer");

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
            DrawText("Diffuse Aydinlatma ile Raytracer", 10, 8, 22, WHITE);
            DrawText("Ambient:0.2 + Point(2,1,0):0.6 + Directional(1,4,4):0.2",
                     10, 33, 14, LIGHTGRAY);
        EndDrawing();
    }

    UnloadTexture(tex);
    CloseWindow();
    return 0;
}
