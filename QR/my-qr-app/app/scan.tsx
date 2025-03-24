import { useEffect, useState, useRef } from "react";
import { StyleSheet, Text, View } from "react-native";
import { Camera, CameraView } from "expo-camera";
import { useRouter } from "expo-router";

export default function Scan() {
  const [hasPermission, setHasPermission] = useState<boolean | null>(null);
  const router = useRouter();
  const hasScanned = useRef(false); // ✅ Prevent multiple navigations

  useEffect(() => {
    (async () => {
      const { status } = await Camera.requestCameraPermissionsAsync();
      setHasPermission(status === "granted");
    })();
  }, []);

  const handleBarcodeScanned = (result: { data: string }) => {
    // Navigate only if no barcode has been processed yet
    if (!hasScanned.current) {
      hasScanned.current = true; // Set flag to prevent duplicate navigation
      router.push({
        pathname: "/show_code",
        params: { data: result.data },
      });
    }
  };

  if (hasPermission === null) return <Text>Solicitando permisos...</Text>;
  if (hasPermission === false) return <Text>Permiso de cámara denegado</Text>;

  return (
    <View style={styles.container}>
      <CameraView
        style={styles.camera}
        barcodeScannerSettings={{
          barcodeTypes: [
            "aztec", "ean13", "ean8", "qr", "pdf417", "upc_e", "datamatrix",
            "code39", "code93", "itf14", "codabar", "code128", "upc_a",
          ],
        }}
        onBarcodeScanned={handleBarcodeScanned}
      />
    </View>
  );
}

const styles = StyleSheet.create({
  container: { flex: 1 },
  camera: { flex: 1 },
});
