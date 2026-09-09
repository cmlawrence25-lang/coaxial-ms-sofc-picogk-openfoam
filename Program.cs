using PicoGK;
using System.Numerics;

namespace CoaxialMS_SOFC;

internal static class Program
{
    private static void Main()
    {
        using Library library = new(0.2f);
        GenerateMsStack(library);
    }

    private static void GenerateMsStack(Library library)
    {
        const float outerDiameter = 200f;
        const float length = 180f;
        const float tubeOuterDiameter = 8f;
        const int tubeCount = 19;
        const float ringRadius = 70f;

        Voxels hotbox = CreateCylinder(library, Vector3.Zero, length, outerDiameter / 2);

        Voxels tubeBundle = new Voxels();
        for (int index = 0; index < tubeCount; index++)
        {
            float angle = (float)index / tubeCount * MathF.PI * 2;
            float x = MathF.Cos(angle) * ringRadius;
            float y = MathF.Sin(angle) * ringRadius;

            Voxels tube = CreateCylinder(library, new Vector3(x, y, 0), length, tubeOuterDiameter / 2);
            tubeBundle += tube;
        }

        Voxels reactor = hotbox - tubeBundle;
        reactor.mshAsMesh().SaveToStlFile("CoaxialMS_SOFC_200mm.stl");
        Library.Log("STL exported successfully: CoaxialMS_SOFC_200mm.stl");
    }

    private static Voxels CreateCylinder(Library library, Vector3 center, float length, float radius)
    {
        Vector3 boundsMin = center - new Vector3(radius, radius, length / 2);
        Vector3 boundsMax = center + new Vector3(radius, radius, length / 2);
        return new Voxels(library, new FiniteCylinder(center, length / 2, radius), new BBox3(boundsMin, boundsMax));
    }

    private sealed class FiniteCylinder : IImplicit
    {
        private readonly Vector3 center;
        private readonly float halfLength;
        private readonly float radius;

        public FiniteCylinder(Vector3 center, float halfLength, float radius)
        {
            this.center = center;
            this.halfLength = halfLength;
            this.radius = radius;
        }

        public float fSignedDistance(in Vector3 point)
        {
            Vector3 local = point - center;
            float radialDistance = MathF.Sqrt(local.X * local.X + local.Y * local.Y) - radius;
            float axialDistance = MathF.Abs(local.Z) - halfLength;
            float outsideDistance = MathF.Sqrt(
                MathF.Max(radialDistance, 0) * MathF.Max(radialDistance, 0) +
                MathF.Max(axialDistance, 0) * MathF.Max(axialDistance, 0));
            return outsideDistance + MathF.Min(MathF.Max(radialDistance, axialDistance), 0);
        }
    }
}