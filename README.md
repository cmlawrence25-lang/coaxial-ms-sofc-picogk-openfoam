# coaxial-ms-sofc-picogk-openfoam

PicoGK voxel geometry generator for a coaxial MS-SOFC reactor stack. The
generator creates a 200 mm diameter, 180 mm long hotbox with 19 tube passages
and exports the resulting solid as an STL for downstream OpenFOAM meshing.

## Requirements

- .NET 9 SDK
- Internet access on the first build so NuGet can restore PicoGK 2.3.0

## Generate the STL

```powershell
dotnet run --project .\CoaxialMS_SOFC.csproj
```

The output file `CoaxialMS_SOFC_200mm.stl` is written to the working directory.
