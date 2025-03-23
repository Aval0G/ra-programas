import React, { useState } from 'react';
import { View, Text, TextInput, Button, StyleSheet, Picker } from 'react-native';
import QRCode from 'react-native-qrcode-svg'; // Para generar QR
import Barcode from 'react-native-barcode-builder'; // Para generar códigos de barras

export default function Generate() {
  const [text, setText] = useState('');
  const [barcodeType, setBarcodeType] = useState('QR'); // Tipo de código
  const [generatedCode, setGeneratedCode] = useState<JSX.Element | null>(null);

  // Función para generar el código basado en el tipo
  const generateCode = () => {
    if (!text) {
      alert('Por favor ingrese el texto para generar el código');
      return;
    }

    if (barcodeType === 'QR') {
      setGeneratedCode(<QRCode value={text} size={200} />);
    } else if (barcodeType === 'EAN13') {
      setGeneratedCode(<Barcode value={text} format="EAN13" />);
    } else if (barcodeType === 'UPC') {
      setGeneratedCode(<Barcode value={text} format="UPC" />);
    } else {
      alert('Tipo de código no soportado');
    }
  };

  return (
    <View style={styles.container}>
      <Text style={styles.title}>Generador de Códigos</Text>
      
      <TextInput
        style={styles.input}
        placeholder="Ingrese el texto"
        value={text}
        onChangeText={setText}
      />

      <Picker
        selectedValue={barcodeType}
        style={styles.picker}
        onValueChange={(itemValue) => setBarcodeType(itemValue)}
      >
        <Picker.Item label="Código QR" value="QR" />
        <Picker.Item label="Código de barras EAN13" value="EAN13" />
        <Picker.Item label="Código de barras UPC" value="UPC" />
      </Picker>

      <Button title="Generar Código" onPress={generateCode} />

      <View style={styles.codeContainer}>
        {generatedCode}
      </View>
    </View>
  );
}

const styles = StyleSheet.create({
  container: { flex: 1, justifyContent: 'center', alignItems: 'center' },
  title: { fontSize: 24, fontWeight: 'bold' },
  input: { width: 250, padding: 10, marginVertical: 20, borderWidth: 1, borderRadius: 5 },
  picker: { width: 250, marginVertical: 20 },
  codeContainer: { marginTop: 20 },
});
